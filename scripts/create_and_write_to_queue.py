import json
import gzip
import localstack_client.session as boto3

QUEUE_NAME = "login-queue"


def send_messages():
    sqs = boto3.client("sqs")
    queue_url = sqs.create_queue(QueueName=QUEUE_NAME)["QueueUrl"]
    print(f"queue_url: [{queue_url}]")

    with gzip.open("/tmp/data/sample_data.json.gz", "r") as f:
        data = json.load(f)

    assert len(data) == 100

    for record in data:
        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(record))

    return


def main():
    send_messages()


if __name__ == "__main__":
    main()
