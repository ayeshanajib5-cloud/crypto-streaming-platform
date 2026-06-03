output "api_repository_url" {
  value = aws_ecr_repository.api.repository_url
}

output "producer_repository_url" {
  value = aws_ecr_repository.producer.repository_url
}

output "spark_repository_url" {
  value = aws_ecr_repository.spark.repository_url
}

output "airflow_repository_url" {
  value = aws_ecr_repository.airflow.repository_url
}