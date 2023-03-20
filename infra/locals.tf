
locals {

  project_name = lower("CloudLog")

  region = "eu-central-1"
  db_table = {
    name = "logs_store"
  }

  frontend = {
    url        = "sniffer.${local.project_name}.com"
    build_path = "../log_sniffer/build"
  }

  lambda = {
    handler = "main.handler"

    read_lambda = {
      source = "../lambda/read_logs/read_logs"
    }

    save_lambda = {
      source = "../lambda/save_logs/save_logs"
    }

    common_layer = {
      name   = "cloudlog_commons"
      source = "../cloudlog_commons"
    }
  }

}