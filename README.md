# About

This repository showcases how to deploy a EMR Serverless application
and run word count as example batch job using it.

# Pre-requisites

* An AWS account
* A S3 bucket named `tfstate-emr-serverless-wordcount-example` exists in the AWS account

# How to deploy

1. Run `aws login`
2. Run `terraform init`
3. Run `terraform apply`