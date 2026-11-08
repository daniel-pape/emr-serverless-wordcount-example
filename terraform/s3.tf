# ==================================================
# Declares two S3 buckets, one for the word count
# script (or in general other scripts to be run)
# and one for the input data. The sample script and
# input data are uploaded using aws_s3_object resources
# ==================================================
resource "aws_s3_bucket" "scripts" {
  bucket = "scripts---${var.project_name}"
}

resource "aws_s3_bucket" "input" {
  bucket = "input---${var.project_name}"
}

resource "aws_s3_object" "main_file" {
  bucket = aws_s3_bucket.scripts.id
  key    = "main.py"
  source = "${path.module}/../src/emr_serverless_wordcount_example/main.py"

  etag = filemd5("${path.module}/../src/emr_serverless_wordcount_example/main.py")
}

resource "aws_s3_object" "input_file" {
  bucket = aws_s3_bucket.input.id
  key    = "input.txt"
  source = "${path.module}/../src/data/input.txt"

  etag = filemd5("${path.module}/../src/data/input.txt")
}
