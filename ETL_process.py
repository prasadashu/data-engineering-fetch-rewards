import boto3
import json
import base64
import psycopg2
from datetime import datetime, timezone

class ETL_Process():
    """Class for performing ETL Process"""

    def __init__(self):
        """Constructor"""
        return

    def base64_encode(self, plain_string):
        """Function to encode string into base64"""
        
        # Encode string to ASCII value
        ascii_string = plain_string.encode('ascii')

        # Encode ASCII string to base64
        encoded_string = base64.b64encode(ascii_string).decode('utf-8')

        return encoded_string

    def get_messages(self):
        """Function to receive messages from SQS Queue"""

        # Instantiate SQS Client
        sqs_client = boto3.client("sqs", endpoint_url = "http://localhost:4566")

        # Receive messages from queue
        response = sqs_client.receive_message(
            QueueUrl="http://localhost:4566/000000000000/login-queue",
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10
        )

        # Get messages from SQS
        messages = response['Messages']
        
        # Return from function
        return messages

    def transform_data(self, messages):
        """Function to transform PII data"""

        # Decalre empty message list
        message_list = []

        # Iterate through the messages
        for message in messages:
            # Get "Body" of the message into JSON/Dictionary format
            message_body = json.loads(message['Body'])

            # Get "ip" and "device_id" of message
            ip = message_body['ip']
            device_id = message_body['device_id']

            # Encode "ip" and "device_id"
            base64_ip = self.base64_encode(ip)
            base64_device_id = self.base64_encode(device_id)

            # Replace "ip" and "device_id" with encoded values
            message_body['ip'] = base64_ip
            message_body['device_id'] = base64_device_id
            
            message_list.append(message_body)

        # Return from function
        return message_list

    def load_data_postgre(self, message_list):
        """Function to load data to postgres"""

        # Connect to PostgreSQL
        postgres_conn = psycopg2.connect(
            host = 'localhost',
            database = 'postgres',
            user = 'postgres',
            password = 'postgres'
        )

        # Create a Cursor
        cursor = postgres_conn.cursor()

        # Iterate through messages
        for message_json in message_list:
            # Remove 'None Type' values
            message_json['locale'] = 'None' if message_json['locale'] == None else message_json['locale']
            # Set 'create_date' field as current date
            message_json['create_date'] = datetime.now().strftime("%Y-%m-%d")

            # Convert dictionary values to list
            values = list(message_json.values())

            # Execute the insert query
            cursor.execute("INSERT INTO user_logins ( \
                user_id, \
                app_version, \
                device_type, \
                masked_ip, \
                locale, \
                masked_device_id, \
                create_date \
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)", values)

            # Commit data to Postgres
            postgres_conn.commit()

        return

def main():
    """The Main Function"""

    # Invoke an object for the class
    etl_process_object = ETL_Process()

    # Extract messages from SQS Queue
    messages = etl_process_object.get_messages()

    # Transform IIPs from the messages
    message_list = etl_process_object.transform_data(messages)

    # Load data to Postgres
    etl_process_object.load_data_postgre(message_list)


# Calling the main function
if __name__ == "__main__":
    main()