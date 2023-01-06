#!/bin/bash

aws configure set profile.default.aws_access_key_id data_engineering_id_key
aws configure set profile.default.aws_secret_access_key data_engineering_secret_key
aws configure set profile.default.region us-east-1