

resource "aws_dynamodb_table" "logs_table" {
  name           = local.db_table.name
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "id"
  range_key      = "timestamp"

  local_secondary_index {
    name = "hostname"
    range_key = "hostname"
    projection_type = "ALL"
  }

  local_secondary_index {
    name = "log_type"
    range_key = "log_type"
    projection_type = "ALL"
  }

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "N"
  }

  attribute {
    name = "log_type"
    type = "S"
  }

  attribute {
    name = "hostname"
    type = "S"
  }

  # attribute {
  #   name = "unit"
  #   type = "S"
  # }

  # attribute {
  #   name = "message"
  #   type = "S"
  # }

  # attribute {
  #   name = "severity"
  #   type = "S"
  # }

  # attribute {
  #   name = "os"
  #   type = "S"
  # }

  # attribute {
  #   name = "raw"
  #   type = "S"
  # }

}
