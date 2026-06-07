terraform {
  backend "s3" {
    bucket         = "crypto-streaming-terraform-state"
    key            = "eks/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "crypto-streaming-terraform-locks"
    encrypt        = true
  }
}