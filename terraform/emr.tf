resource "aws_emrserverless_application" "serverless_emr_app" {
  name          = "serverless-emr-app"
  release_label = var.emr_release
  type          = "SPARK"

  runtime_configuration {
    classification = "spark-defaults"

    properties = {
      "spark.dynamicAllocation.enabled" = "false"
      "spark.executor.cores"             = "1"
      "spark.executor.memory"            = "4g"
      "spark.driver.cores"               = "1"
      "spark.driver.memory"              = "4g"
      "spark.executor.instances"         = "1"
    }
  }

  # Don't keep the application running when it is not being used.
  auto_start_configuration {
    enabled = true
  }

  auto_stop_configuration {
    enabled              = true
    idle_timeout_minutes = 5
  }

  # Hard limit on resources that the application can consume.
  maximum_capacity {
    cpu    = "2 vCPU"
    memory = "10 GB"
    disk   = "40 GB"
  }

  tags = {
    Name        = "serverless-emr-app"
    ManagedBy   = "terraform"
  }
}