#!/bin/bash

if ! command -v poetry &> /dev/null; then
    echo "You need to install poetry to run this script"
    exit
fi

if ! command -v poetry run pytest &> /dev/null; then
    echo "Installing pytest"
    poetry add pytest
fi

echo "testing ..."

poetry run pytest ./cloud_logger
poetry run pytest ./cloudlog_commons
poetry run pytest ./lambda/read_logs
poetry run pytest ./lambda/save_logs
poetry run pytest ./logger_daemon

echo "Testing Successfull !"

set -e

if ! command -v terraform &> /dev/null; then
    echo "The 'terraform' is not installed. Install it to continue the deployment"
    exit
fi

if ! command -v aws &> /dev/null; then
    echo "The 'aws'/'aws-cli' is not installed. Install it to continue the deployment"
    exit
fi

cd infra
terraform validate
# terraform apply

echo "Infrastrucutre deployment done"

cd ../log_sniffer
npm run build

cd ./build
aws s3 rm --recursive s3://sniffer.cloudlog.com/*
aws s3 cp --recursive ./. s3://sniffer.cloudlog.com

echo "LogSniffer deployment done"