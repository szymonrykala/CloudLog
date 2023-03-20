

data "external" "manage_proper_dir_structure_for_layer" {
  working_dir = local.lambda.common_layer.source
  program = ["sh", "-c", <<-EOF
    mkdir python
    cp -r ${local.lambda.common_layer.name} python/${local.lambda.common_layer.name}

    jq "{}" #dummy output
  EOF
  ]

  query = {}
}

data "archive_file" "common_libs_zip" {
  type       = "zip"
  source_dir = local.lambda.common_layer.source
  excludes = [
    "tests",
    "cloudlog_commons",
    "pyproject.toml",
    "README.md"
  ]
  output_path = "${local.lambda.common_layer.source}.zip"

  depends_on = [
    data.external.manage_proper_dir_structure_for_layer
  ]
}

resource "aws_lambda_layer_version" "common_libs" {
  filename         = data.archive_file.common_libs_zip.output_path
  layer_name       = local.lambda.common_layer.name
  source_code_hash = data.archive_file.common_libs_zip.output_base64sha256

  compatible_runtimes = ["python3.9"]
}
