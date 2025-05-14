# AWS Terraform Infrastructure for domo-example

This directory contains Terraform files to deploy the infrastructure for the domo-example project, as described in `specifications.md`.

## Components
- Minimal 3 node etcd cluster (EC2)
- Single GPU node for Ollama, Crawler, and ChromaDB (EC2)
- AWS API Gateway and Lambda for POST queries to Ollama
- CloudWatch Event (cron) to trigger crawler every 5 minutes

---

## Prerequisites
- AWS CLI installed and configured with appropriate credentials
- Terraform installed (v1.0+ recommended)
- Python 3.11+ and `pip` installed (for Lambda packaging)
- An S3 bucket for Lambda deployment packages

---

## Step 1: Package the Lambda Functions

Navigate to the Lambda directory:
```sh
cd aws/lambda
```

### Package the API Lambda
```sh
./package_api_lambda.sh
```
This creates `lambda_function.zip` in the same directory.

### Package the Crawler Lambda
```sh
./package_crawler_lambda.sh
```
This creates `crawler_lambda.zip` in the same directory.

---

## Step 2: Upload Lambda Packages to S3

Replace `<your-bucket>` with your S3 bucket name:
```sh
aws s3 cp lambda_function.zip s3://<your-bucket>/lambda/lambda_function.zip
aws s3 cp crawler_lambda.zip s3://<your-bucket>/lambda/crawler_lambda.zip
```

---

## Step 3: Configure Terraform Variables

Edit `aws/terraform.tfvars` (copy from `terraform.tfvars.example` if needed):
```hcl
aws_region = "us-west-2"

lambda_s3_bucket    = "<your-bucket>"
lambda_s3_key       = "lambda/lambda_function.zip"
crawler_lambda_s3_bucket = "<your-bucket>"
crawler_lambda_s3_key    = "lambda/crawler_lambda.zip"

# Set AMI IDs and key names for your region/account
etcd_ami = "ami-xxxxxxxxxxxxxxxxx"
etcd_key_name = "your-ssh-key-name"
gpu_ami = "ami-xxxxxxxxxxxxxxxxx"
gpu_key_name = "your-ssh-key-name"
```

---

## Step 4: Initialize and Apply Terraform

From the `aws/` directory:
```sh
terraform init
terraform plan
terraform apply
```
Terraform will provision all resources, including EC2 instances, security groups, Lambda functions, API Gateway, and CloudWatch Event rules.

---

## Step 5: Verify Deployment
- Check the Terraform outputs for public IPs, API Gateway URL, etc.
- Test the API Gateway endpoint with a POST request.
- Check CloudWatch logs for Lambda execution results.

---

## Notes
- The Lambda functions are packaged with all dependencies using the provided shell scripts.
- The crawler Lambda uses `/tmp` for temporary storage (as required by AWS Lambda).
- Ensure your AMI IDs are correct and support the required features (GPU, etcd, Docker, etc.).
- You may need to adjust IAM permissions, VPC/subnet settings, or security groups for your environment.
- For production, consider versioning your Lambda packages and using more restrictive IAM roles.

---

## Cleanup
To destroy all resources created by Terraform:
```sh
terraform destroy
```

---

For further customization, see `specifications.md` and the comments in each `.tf` file. 