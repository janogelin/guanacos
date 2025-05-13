# outputs.tf

# Output for etcd cluster endpoints
output "etcd_cluster_endpoints" {
  description = "The endpoints of the etcd cluster nodes."
  value       = [] # To be populated
}

# Output for GPU node public IP
output "gpu_node_public_ip" {
  description = "The public IP of the GPU node running Ollama, Crawler, and ChromaDB."
  value       = aws_instance.gpu_node.public_ip
}

# Output for GPU node private IP
output "gpu_node_private_ip" {
  description = "The private IP of the GPU node running Ollama, Crawler, and ChromaDB."
  value       = aws_instance.gpu_node.private_ip
}

# Output for API Gateway endpoint
output "api_gateway_url" {
  description = "The URL of the API Gateway for posting queries to Ollama."
  value       = aws_apigatewayv2_api.ollama_api.api_endpoint
}

output "etcd_public_ips" {
  description = "Public IPs of the etcd cluster nodes."
  value       = aws_instance.etcd[*].public_ip
}

output "etcd_private_ips" {
  description = "Private IPs of the etcd cluster nodes."
  value       = aws_instance.etcd[*].private_ip
} 