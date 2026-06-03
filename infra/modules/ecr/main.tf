resource "aws_ecr_repository" "api" {
  name = "crypto-api"
}

resource "aws_ecr_repository" "producer" {
  name = "crypto-producer"
}

resource "aws_ecr_repository" "spark" {
  name = "crypto-spark"
}

resource "aws_ecr_repository" "airflow" {
  name = "crypto-airflow"
}