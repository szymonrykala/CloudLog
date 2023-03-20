

resource "aws_iam_role" "lambda_role" {
  name = "${var.name}_iam_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}


resource "aws_iam_policy" "lambda_logging" {
  name = "${var.name}_iam_role"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_logs_attachment" {
  policy_arn = aws_iam_policy.lambda_logging.arn
  role       = aws_iam_role.lambda_role.name
}

resource "aws_iam_policy" "lambda_user_policy" {
  name        = "${var.name}_user_defined_policy"
  path        = "/"
  description = "IAM policy for user specified actions"
  policy      = var.access_policy
}

resource "aws_iam_role_policy_attachment" "user_policy_attachment" {
  policy_arn = aws_iam_policy.lambda_user_policy.arn
  role       = aws_iam_role.lambda_role.name
}


data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = var.source_code
  output_path = "${var.source_code}.zip"
  excludes = var.excludes
}

resource "aws_lambda_function" "lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = data.archive_file.lambda.output_path
  function_name = var.name
  role          = aws_iam_role.lambda_role.arn
  handler       = var.handler

  source_code_hash = data.archive_file.lambda.output_base64sha256

  runtime = var.runtime
  layers  = var.layers

  environment {
    variables = var.environment
  }
}

resource "aws_cloudwatch_log_group" "service_logs" {
  name              = "/aws/lambda/${var.name}"
  retention_in_days = 14
}
