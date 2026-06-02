output "cluster_name" {
  value = module.eks.cluster_name
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "api_ecr_repository_url" {
  value = aws_ecr_repository.api.repository_url
}

output "producer_ecr_repository_url" {
  value = aws_ecr_repository.producer.repository_url
}

output "spark_ecr_repository_url" {
  value = aws_ecr_repository.spark.repository_url
}

output "airflow_ecr_repository_url" {
  value = aws_ecr_repository.airflow.repository_url
}