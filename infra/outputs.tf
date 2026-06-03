output "cluster_name" {
  value = module.eks_cluster.cluster_name
}

output "cluster_endpoint" {
  value = module.eks_cluster.cluster_endpoint
}

output "vpc_id" {
  value = module.networking.vpc_id
}

output "api_ecr_repository_url" {
  value = module.ecr.api_repository_url
}

output "producer_ecr_repository_url" {
  value = module.ecr.producer_repository_url
}

output "spark_ecr_repository_url" {
  value = module.ecr.spark_repository_url
}

output "airflow_ecr_repository_url" {
  value = module.ecr.airflow_repository_url
}

output "cloudwatch_log_group_name" {
  value = module.cloudwatch.log_group_name
}