resource "aws_s3_bucket" "scripts" {
  bucket = "scripts---${var.project_name}"
}

resource "aws_s3_bucket" "input" {
  bucket = "input---${var.project_name}"
}

resource "aws_s3_bucket" "output" {
  bucket = "output---${var.project_name}"
}