

resource "aws_s3_bucket" "app_hosting" {
  bucket = local.frontend.url
}

resource "aws_s3_bucket_acl" "example_bucket_acl" {
  bucket = aws_s3_bucket.app_hosting.id
  acl    = "public-read"
}

resource "aws_s3_bucket_website_configuration" "example" {
  bucket = aws_s3_bucket.app_hosting.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }

  #   routing_rule {
  #     condition {
  #       key_prefix_equals = "/"
  #     }
  #     redirect {
  #       replace_key_prefix_with = "documents/"
  #     }
  #   }
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
