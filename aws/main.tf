# main.tf

provider "aws" {
  region = var.aws_region
}

# ---
# 1. Minimal 3 node etcd cluster (EC2 instances)
resource "aws_security_group" "etcd" {
  name        = "etcd-cluster-sg"
  description = "Allow etcd and SSH access"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "Allow etcd peer communication"
    from_port   = 2379
    to_port     = 2380
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids" "default" {
  vpc_id = data.aws_vpc.default.id
}

resource "aws_instance" "etcd" {
  count         = var.etcd_cluster_size
  ami           = var.etcd_ami
  instance_type = var.etcd_instance_type
  key_name      = var.etcd_key_name
  subnet_id     = element(data.aws_subnet_ids.default.ids, count.index % length(data.aws_subnet_ids.default.ids))
  vpc_security_group_ids = [aws_security_group.etcd.id]
  tags = {
    Name = "etcd-node-${count.index + 1}"
    Role = "etcd"
  }
  # User data for etcd installation/configuration can be added here
}

# 2. Single GPU node for Ollama, Crawler, and ChromaDB (EC2 instance)
resource "aws_security_group" "gpu_node" {
  name        = "gpu-node-sg"
  description = "Allow SSH, Ollama API, and ChromaDB access"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "Allow SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Ollama API (default 11434)"
    from_port   = 11434
    to_port     = 11434
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "ChromaDB (default 8000)"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "gpu_node" {
  ami           = var.gpu_ami
  instance_type = var.gpu_instance_type
  key_name      = var.gpu_key_name
  subnet_id     = element(data.aws_subnet_ids.default.ids, 0)
  vpc_security_group_ids = [aws_security_group.gpu_node.id]
  tags = {
    Name = "gpu-node-ollama"
    Role = "ollama-gpu"
  }
  # User data for Docker, Ollama, Crawler, and ChromaDB setup can be added here
}

# 3. API Gateway and Lambda for POST queries to Ollama
resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "ollama_api" {
  function_name = var.lambda_function_name
  s3_bucket     = var.lambda_s3_bucket
  s3_key        = var.lambda_s3_key
  handler       = var.lambda_handler
  runtime       = var.lambda_runtime
  role          = aws_iam_role.lambda_exec.arn
  timeout       = 30
  environment {
    variables = {
      OLLAMA_HOST = aws_instance.gpu_node.public_ip
    }
  }
}

resource "aws_apigatewayv2_api" "ollama_api" {
  name          = var.api_gateway_name
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id                 = aws_apigatewayv2_api.ollama_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.ollama_api.invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "post_route" {
  api_id    = aws_apigatewayv2_api.ollama_api.id
  route_key = "POST /ollama"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.ollama_api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_lambda_permission" "apigw_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ollama_api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.ollama_api.execution_arn}/*/*"
}

# 4. CloudWatch Event (cron) to trigger crawler every 5 minutes
resource "aws_lambda_function" "crawler" {
  function_name = var.crawler_lambda_function_name
  s3_bucket     = var.crawler_lambda_s3_bucket
  s3_key        = var.crawler_lambda_s3_key
  handler       = var.crawler_lambda_handler
  runtime       = var.crawler_lambda_runtime
  role          = aws_iam_role.lambda_exec.arn
  timeout       = 300
  environment {
    variables = {
      ETCD_HOST = join(",", aws_instance.etcd[*].private_ip)
      CHROMADB_HOST = aws_instance.gpu_node.private_ip
      # Add other environment variables as needed
    }
  }
}

resource "aws_cloudwatch_event_rule" "crawler_schedule" {
  name                = "crawler-schedule-rule"
  schedule_expression = var.crawler_cron_schedule
}

resource "aws_cloudwatch_event_target" "crawler_lambda_target" {
  rule      = aws_cloudwatch_event_rule.crawler_schedule.name
  target_id = "crawler-lambda"
  arn       = aws_lambda_function.crawler.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_invoke_crawler" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.crawler.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.crawler_schedule.arn
} 