terraform {
  backend "s3" {
    bucket         = "crypto-streaming-terraform-state-504429674609"
    key            = "eks/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "crypto-streaming-terraform-locks"
    encrypt        = true
  }
}