
resource "aws_default_vpc" "default" {
  tags = {
    Name = "VPC"
  }
}

resource "aws_default_subnet" "eu_central_1a" {
  availability_zone = "eu-central-1a"

  tags = {
    Name = "Default subnet for eu-central-1"
  }
}

resource "aws_default_subnet" "eu_central_1b" {
  availability_zone = "eu-central-1b"

  tags = {
    Name = "Default subnet for eu-central-1"
  }
}
