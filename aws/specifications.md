# Project Specifications: domo-example Terraform Deployment

## Goals
Create domo-example terraform files that launch the following instances:

1. **A minimal 3 node cluster of etcd**
2. **A single GPU node** that can handle the biggest Gemma model running Ollama
3. **An AWS API Gateway** that can post queries to Ollama

---

## Specifications

1. Use the music lover version of the Ollama code in Ollama chat to integrate with the API Gateway
2. Write the AWS API Gateway as a Lambda function in Python
3. Create appropriate Terraform files for all infrastructure
4. Only allow POST requests to the API and create the response object for the API
5. Create a cron in the Terraform file for the Ollama server that will run the crawler every 5 minutes and store the embeddings in ChromaDB
6. Crawler should use the etcd specified in goals
7. Crawler and ChromaDB can run on the same node as the GPU server 