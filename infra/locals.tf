
locals {

  project_name = lower("CloudLog")

  region = "eu-central-1"
  db_table = {
    name = "logs_store"
    username = "cloudlog_root"
  }

  frontend = {
    url        = "sniffer.${local.project_name}.com"
    build_path = "../log_sniffer/build"
  }

  lambda = {
    handler = "main.handler"

    read_lambda = {
      source = "../lambda/read_logs/"
      env = {
        HTTP_REQUEST_ORIGIN = "http://${aws_s3_bucket_website_configuration.app_hosting.website_endpoint}"
      }
    }

    save_lambda = {
      source = "../lambda/save_logs/"
    }

    common_layer = {
      name   = "cloudlog_commons"
      source = "../cloudlog_commons"
    }
  }

}