terraform {
  backend "s3" {
    bucket = "tfstate-emr-serverless-wordcount-example"
    key    = "./terraform.tfstate"
    region = "eu-central-1"
  }
}