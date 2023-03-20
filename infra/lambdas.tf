
data "archive_file" "common_libs_zip" {
  type        = "zip"
  source_dir  = local.lambda.common_layer.source
  excludes    = ["${local.lambda.common_layer.source}/tests/*"]
  output_path = "${local.lambda.common_layer.source}.zip"
}

resource "aws_lambda_layer_version" "common_libs" {
  filename   = data.archive_file.common_libs_zip.output_path
  layer_name = local.lambda.common_layer.name
  source_code_hash = data.archive_file.common_libs_zip.output_base64sha256

  compatible_runtimes = ["python3.9"]

}


data "aws_iam_policy_document" "read_logs_role" {
  statement {
    effect = "Allow"

    resources = [
      resource.aws_dynamodb_table.logs_table.arn
    ]

    actions = [
      "dynamodb:BatchGetItem",
      "dynamodb:GetRecords",
      "dynamodb:GetItem"
    ]
  }
}

module "read_logs_lambda" {
  source        = "./modules/lambda_service"
  name          = "read_logs"
  access_policy = data.aws_iam_policy_document.read_logs_role.json
  handler       = local.lambda.handler

  source_code   = local.lambda.read_lambda.source
  layers        = [aws_lambda_layer_version.common_libs.arn]
  environment = {
    "MAX_COUNT" = "50"
  }
}


data "aws_iam_policy_document" "save_logs_role" {
  statement {
    effect = "Allow"

    resources = [
      resource.aws_dynamodb_table.logs_table.arn
    ]

    actions = [
      "dynamodb:BatchWriteItem",
      "dynamodb:PutItem"
    ]
  }
}

module "save_logs_lambda" {
  source        = "./modules/lambda_service"
  name          = "save_logs"
  source_code   = local.lambda.save_lambda.source
  handler       = local.lambda.handler
  access_policy = data.aws_iam_policy_document.save_logs_role.json
  layers        = [aws_lambda_layer_version.common_libs.arn]
  environment = {
    "SAVE_LOGS" = "false"
  }
}



