#!/bin/bash

check_command_exist(){
    if ! command -v $1 &> /dev/null; then
        echo "You need to install $1 to run this script"
        exit
    fi
}

required_binaries=(poetry terraform aws)
poetry_projects=(./cloudlog_commons/ ./cloud_logger/ ./lambda/read_logs/ ./lambda/save_logs/ ./logger_daemon/)


echo "Checking environment ..."
for binary in "${required_binaries[@]}"; do
    check_command_exist $binary
done

set -e

echo "Testing ..."
for project in "${poetry_projects[@]}"; do
    cd $project
    if ! grep pytest ./pyproject.toml; then
        echo "Installing pytest"
        poetry add "pytest=7.3.0"
    fi

    echo "Testing $project"
    poetry run pytest -v --disable-warnings
    cd -
done
echo "Tests are Successfull!"


echo "Managing infrastructure..."

cd infra
terraform validate
terraform apply

echo "Infrastrucutre deployment done"

# exit #temporary

cd ../log_sniffer
npm run build

cd ./build
aws s3 rm --recursive s3://sniffer.cloudlog.com/*
aws s3 cp --recursive ./. s3://sniffer.cloudlog.com

echo "LogSniffer deployment done"