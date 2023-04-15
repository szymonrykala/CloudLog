
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.63.0"
    }
  }

  backend "s3" {
    bucket = "tfstate-cloudlog"
    key    = "tfstate"
    region = "eu-central-1"
  }
}

provider "aws" {
  region                   = local.region
  profile                  = "default"
  shared_credentials_files = ["~/.aws/credentials"]
}

data "aws_region" "current" {}
data "aws_caller_identity" "current" {}