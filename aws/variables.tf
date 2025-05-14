# variables.tf

variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-west-2"
}

variable "etcd_instance_type" {
  description = "EC2 instance type for etcd nodes."
  type        = string
  default     = "t3.small"
}

variable "etcd_ami" {
  description = "AMI ID for etcd nodes. Should be a minimal Linux AMI."
  type        = string
}

variable "etcd_key_name" {
  description = "SSH key name for etcd nodes."
  type        = string
}

variable "etcd_cluster_size" {
  description = "Number of nodes in the etcd cluster."
  type        = number
  default     = 3
}

variable "gpu_instance_type" {
  description = "EC2 instance type for the GPU node."
  type        = string
  default     = "g4dn.xlarge"
}

variable "gpu_ami" {
  description = "AMI ID for the GPU node. Should support NVIDIA GPU and Docker."
  type        = string
}

variable "gpu_key_name" {
  description = "SSH key name for the GPU node."
  type        = string
}

variable "lambda_function_name" {
  description = "Name for the Ollama API Lambda function."
  type        = string
  default     = "ollama-api-handler"
}

variable "lambda_handler" {
  description = "Handler for the Lambda function."
  type        = string
  default     = "lambda_function.lambda_handler"
}

variable "lambda_runtime" {
  description = "Runtime for the Lambda function."
  type        = string
  default     = "python3.11"
}

variable "lambda_s3_bucket" {
  description = "S3 bucket for Lambda deployment package."
  type        = string
}

variable "lambda_s3_key" {
  description = "S3 key for Lambda deployment package."
  type        = string
}

variable "api_gateway_name" {
  description = "Name for the API Gateway."
  type        = string
  default     = "ollama-api-gateway"
}

variable "crawler_lambda_function_name" {
  description = "Name for the crawler Lambda function."
  type        = string
  default     = "music-crawler-handler"
}

variable "crawler_lambda_handler" {
  description = "Handler for the crawler Lambda function."
  type        = string
  default     = "crawler_lambda.lambda_handler"
}

variable "crawler_lambda_runtime" {
  description = "Runtime for the crawler Lambda function."
  type        = string
  default     = "python3.11"
}

variable "crawler_lambda_s3_bucket" {
  description = "S3 bucket for crawler Lambda deployment package."
  type        = string
}

variable "crawler_lambda_s3_key" {
  description = "S3 key for crawler Lambda deployment package."
  type        = string
}

variable "crawler_cron_schedule" {
  description = "Cron expression for running the crawler (default: every 5 minutes)."
  type        = string
  default     = "cron(0/5 * * * ? *)"
}

# Add more variables as needed for instance types, AMIs, etc. 