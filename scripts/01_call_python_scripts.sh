#!/bin/sh

echo "downloding localstack dependency"
pip install localstack-client

echo  "starting python script"
python /tmp/scripts/create_and_write_to_queue.py

echo "winding down"
