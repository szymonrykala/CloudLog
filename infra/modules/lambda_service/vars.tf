
variable "name" {
  description = "lambda function name"
  type        = string
}

variable "source_code" {
  description = "path to source code"
  type        = string
}

variable "handler" {
  description = "starting point of the function"
}

variable "excludes" {
  description = "list of zip excluded files"
  type        = list(string)
  default     = ["tests", ".pytest_cache", "README.md", "poetry.lock"]
}

variable "layers" {
  description = "arn's of the lambda layers"
  type        = list(string)
  default     = []
}

variable "environment" {
  description = "map of env variables"
  type        = map(string)
  default     = {}
}

variable "access_policy" {
  description = "the aws_iam_policy_document json"
  type        = string
}

variable "runtime" {
  description = "lambda runtime"
  type        = string
  default     = "python3.9"
}