
data "aws_iam_policy_document" "read_logs_role" {
  statement {
    effect = "Allow"

    resources = [
      resource.aws_dynamodb_table.logs_table.arn
    ]

    actions = [
      "dynamodb:BatchGetItem",
      "dynamodb:Query",
      "dynamodb:Scan"
    ]
  }
}

module "read_logs_lambda" {
  source        = "./modules/lambda_service"
  name          = "read_logs"
  access_policy = data.aws_iam_policy_document.read_logs_role.json
  handler       = "read_logs.${local.lambda.handler}"

  source_code = local.lambda.read_lambda.source
  layers      = [aws_lambda_layer_version.common_libs.arn]
  environment = merge(
    local.lambda.read_lambda.env,
    {
      DYNAMO_TABLE_NAME = aws_dynamodb_table.logs_table.name
      MAX_COUNT         = "50"
    }
  )
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

  statement {
    effect = "Allow"

    resources = [
      resource.aws_sqs_queue.logs_buffer.arn
    ]

    actions = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes"
    ]
  }

}

module "save_logs_lambda" {
  source      = "./modules/lambda_service"
  name        = "save_logs"
  source_code = local.lambda.save_lambda.source
  handler     = "save_logs.${local.lambda.handler}"

  access_policy = data.aws_iam_policy_document.save_logs_role.json
  layers        = [aws_lambda_layer_version.common_libs.arn]
  environment = {
    SAVE_LOGS         = "false"
    DYNAMO_TABLE_NAME = aws_dynamodb_table.logs_table.name
  }
}

resource "aws_lambda_event_source_mapping" "save_lambda" {
  event_source_arn = aws_sqs_queue.logs_buffer.arn
  function_name    = module.save_logs_lambda.arn

  batch_size                         = 10
  maximum_batching_window_in_seconds = 60
}

