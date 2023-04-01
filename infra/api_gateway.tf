
resource "aws_api_gateway_rest_api" "cloudlog" {
  name        = "${local.project_name}-api"
  description = "HTTP REST api for ${local.project_name}"

  body = templatefile("./openapi/cloudlog_api.yaml", {
    get_logs_arn           = module.read_logs_lambda.arn,
    logs_buffer_queue_name = aws_sqs_queue.logs_buffer.name,
    gateway_iam_role       = aws_iam_role.gateway_role.arn,
    region                 = data.aws_region.current.name,
    account_id             = data.aws_caller_identity.current.id
  })

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}


resource "aws_api_gateway_deployment" "cloudlog" {
  rest_api_id = aws_api_gateway_rest_api.cloudlog.id

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.cloudlog.body))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "cloudlog_dev" {
  deployment_id = aws_api_gateway_deployment.cloudlog.id
  rest_api_id   = aws_api_gateway_rest_api.cloudlog.id
  stage_name    = "dev"
}



data "aws_iam_policy_document" "cloudlog_api_policy_doc" {
  statement {
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    actions   = ["lambda:Invoke"]
    resources = [module.read_logs_lambda.arn]
  }
}
resource "aws_api_gateway_rest_api_policy" "cloudlog_api_policy" {
  rest_api_id = aws_api_gateway_rest_api.cloudlog.id
  policy      = data.aws_iam_policy_document.cloudlog_api_policy_doc.json
}

resource "aws_iam_role" "gateway_role" {
  name = "${local.project_name}-gateway-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "apigateway.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy" "api_gateway_policy" {
  name = "api-gateway-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "lambda:InvokeFunctionUrl",
          "lambda:InvokeFunction"
        ]
        Effect   = "Allow"
        Resource = module.read_logs_lambda.arn
      },
      {
        Action = [
          "sqs:SendMessage"
        ]
        Effect   = "Allow"
        Resource = aws_sqs_queue.logs_buffer.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_logs_attachment" {
  policy_arn = aws_iam_policy.api_gateway_policy.arn
  role       = aws_iam_role.gateway_role.name
}
