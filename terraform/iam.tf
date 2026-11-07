# ==================================================
# The runtime role used by the EMR Serverless app.
# It is configured to have the necessary rights
# on the input and script bucket, and has CloudWatch
# log permissions.
# ==================================================
resource "aws_iam_role" "emr_serverless_runtime" {
  name = "emr-serverless-runtime"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "emr-serverless.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "emr_serverless_s3" {
  name = "emr-serverless-s3-access"
  role = aws_iam_role.emr_serverless_runtime.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "s3:ListBucket"
        ]

        Resource = [
          aws_s3_bucket.scripts.arn,
          aws_s3_bucket.input.arn
        ]
      },
      {
        Effect = "Allow"

        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]

        Resource = [
          "${aws_s3_bucket.scripts.arn}/*",
          "${aws_s3_bucket.input.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy" "emr_serverless_logs" {
  name = "emr-serverless-logs"
  role = aws_iam_role.emr_serverless_runtime.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogStreams"
        ]

        Resource = "*"
      }
    ]
  })
}