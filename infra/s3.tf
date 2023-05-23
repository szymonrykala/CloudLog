

data "aws_iam_policy_document" "allow_hosting_access" {
  statement {
    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = [
      "s3:GetObject"
    ]

    resources = [
      "${aws_s3_bucket.app_hosting.arn}/*"
    ]
  }
}

resource "aws_s3_bucket" "app_hosting" {
  bucket = local.frontend.url
}

resource "aws_s3_bucket_policy" "allow_hosting_access_policy" {
  bucket = aws_s3_bucket.app_hosting.id
  policy = data.aws_iam_policy_document.allow_hosting_access.json
}

resource "aws_s3_bucket_acl" "app_hosting_acl" {
  bucket = aws_s3_bucket.app_hosting.id
  acl    = "public-read"
}

resource "aws_s3_bucket_website_configuration" "app_hosting" {
  bucket = aws_s3_bucket.app_hosting.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_s3_bucket_cors_configuration" "app_cors" {
  bucket = aws_s3_bucket.app_hosting.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = ["https://${local.frontend.url}"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }

  cors_rule {
    allowed_methods = ["GET", "PUT"]
    allowed_origins = ["*"]
  }
}
