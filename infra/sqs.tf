

resource "aws_sqs_queue" "logs_buffer" {
  name = "${local.project_name}-logs-buffer"

  message_retention_seconds = 60 * 60 #1h

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.logs_buffer_dlq.arn
    maxReceiveCount     = 10
  })
}

resource "aws_sqs_queue" "logs_buffer_dlq" {
  name = "${local.project_name}-logs-buffer-dlq"
}


data "aws_iam_policy_document" "logs_buffer_policy" {
  statement {
    sid    = "First"
    effect = "Allow"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions   = ["sqs:SendMessage"]
    resources = [aws_sqs_queue.logs_buffer.arn]

    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_api_gateway_rest_api.cloudlog.arn]
    }
  }
}

resource "aws_sqs_queue_policy" "logs_buffer_policy" {
  queue_url = aws_sqs_queue.logs_buffer.id
  policy    = data.aws_iam_policy_document.logs_buffer_policy.json
}