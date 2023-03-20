#!/bin/bash


pip install pytest

echo "testing ..."

pytest ./cloud_logger
pytest ./cloudlog_commons
pytest ./lambda/read_logs
pytest ./lambda/save_logs
pytest ./logger_daemon

echo "Testing Successfull !"

set -e

cd infra
# terraform apply

echo "Infrastrucutre deployment done"

cd ../log_sniffer/build
aws s3 rm --recursive s3://sniffer.cloudlog.com/*
aws s3 cp --recursive ./. s3://sniffer.cloudlog.com

echo "LogSniffer deployment done"