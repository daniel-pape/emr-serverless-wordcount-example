variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "project_name" {
  type = string
  default = "emr-serverless-wordcount-example"
  description = "Name of the project, used to make resource names unique"
}

variable "emr_release" {
  type        = string
  default     = "emr-7.9.0"
  description = "EMR Serverless release."
}
