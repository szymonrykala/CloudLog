

resource "aws_dynamodb_table" "logs_table" {
  name           = local.db_table.name
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "logId"
  range_key      = "day"

  attribute {
    name = "logId"
    type = "S"
  }

  attribute {
    name = "day"
    type = "S"
  }


  #   global_secondary_index {
  #     name               = "GameTitleIndex"
  #     hash_key           = "GameTitle"
  #     range_key          = "TopScore"
  #     write_capacity     = 1
  #     read_capacity      = 1
  #     projection_type    = "INCLUDE"
  #     non_key_attributes = ["UserId"]
  #   }

  tags = {
    Name = local.db_table.name
  }
}
