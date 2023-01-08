import boto3
import json
import base64
import psycopg2
import configparser
import argparse
from datetime import datetime
from botocore import exceptions
from botocore import errorfactory

class ETL_Process():
    """Class for performing ETL Process"""

    def __init__(self, endpoint_url, queue_name, wait_time, max_messages):
        """Constructor to get Postgres credentials"""

        # Instantiate the config parser
        config = configparser.ConfigParser()

        # Read the config file
        config.read('postgres.ini')

        # Get config details
        self.__username = config.get('postgres', 'username')
        self.__password = config.get('postgres', 'password')
        self.__host = config.get('postgres', 'host')
        self.__database = config.get('postgres', 'database')

        # Get argument values
        self.__endpoint_url = endpoint_url
        self.__queue_name = queue_name
        self.__wait_time = wait_time
        self.__max_messages = max_messages

        # Return from the constructor
        return

    def base64_encode(self, string_parameter, action = "encode"):
        """Function to encode or decode string using base64"""

        # Check if action is encoding or decoding
        if action == "encode":
            # Encode string to ASCII value
            ascii_string = string_parameter.encode('ascii')

            # Encode ASCII string to base64
            encoded_string = base64.b64encode(ascii_string).decode('utf-8')

            # Return the encoded string
            return encoded_string

        # Else decode the encrypted string
        elif action == "decode":
            # Decode base64 encrypted string
            decoded_string = base64.b64decode(string_parameter).decode('utf-8')

            # Return the decoded string
            return decoded_string

    def get_messages(self):
        """Function to receive messages from SQS Queue"""

        # Instantiate SQS Client
        sqs_client = boto3.client("sqs", endpoint_url = self.__endpoint_url)

        # Receive messages from queue
        try:
            response = sqs_client.receive_message(
                QueueUrl= self.__endpoint_url + '/' + self.__queue_name,
                MaxNumberOfMessages=self.__max_messages,
                WaitTimeSeconds=self.__wait_time
            )
        except Exception as exceptions:
            # Print error while parsing parameters
            print("Error - " + str(exceptions))

            # Exit from function
            return

        # Get messages from SQS
        messages = response['Messages']
        
        # Return from function
        return messages

    def transform_data(self, messages):
        """Function to transform PII data"""

        # Decalre empty message list
        message_list = []

        # Check if "messages" list is empty
        try:
            if len(messages) == 0:
                # Raise TypeError
                raise TypeError("Message list is empty")
                
        except TypeError as type_error:
            # Print the message is empty
            print("Error - " + str(type_error))

            # Return from the function
            return

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
            
            # Append data to message list
            message_list.append(message_body)

        # Return from function
        return message_list

    def load_data_postgre(self, message_list):
        """Function to load data to postgres"""

        # Check if "message_list" is empty
        try:
            if len(message_list) == 0:
                # Raise Type Error
                raise TypeError
        except TypeError as type_error:
            # Print the "message_list" is empty
            print("Error - " + str(type_error))

            # Return from the function
            return


        # Connect to PostgreSQL
        postgres_conn = psycopg2.connect(
            host = self.base64_encode(self.__host, action="decode"),
            database = self.base64_encode(self.__database, action="decode"),
            user = self.base64_encode(self.__username, action="decode"),
            password = self.base64_encode(self.__password, action="decode")
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

        # Close connection to Postgres
        postgres_conn.close()

        # Return from the function
        return


def main():
    """The Main Function"""

    # Instantiate the argparser
    parser = argparse.ArgumentParser(
        prog = "Extract Transform Load - Process",
        description = "Program extracts data from SQS queue - \
                       Transforms PIIs in the data - \
                       Loads the processed data into Postgres",
        epilog = "Please raise an issue for code modifications"
    )

    # Add arguments
    parser.add_argument('-e', '--endpoint-url', required = True ,help = "Pass the endpoint URL here")
    parser.add_argument('-q', '--queue-name', required = True ,help = "Pass the queue URL here")
    parser.add_argument('-t', '--wait-time', type = int, default = 10, help = "Pass the wait time here")
    parser.add_argument('-m', '--max-messages', type = int, default = 10, help = "Pass the max messages to be pulled from SQS queue here")

    # Parse the arguments
    args = vars(parser.parse_args())

    # Get value for each argument
    endpoint_url = args['endpoint_url']
    queue_name = args['queue_name']
    wait_time = args['wait_time']
    max_messages = args['max_messages']

    # Invoke an object for the class
    etl_process_object = ETL_Process(endpoint_url, queue_name, wait_time, max_messages)

    # Extract messages from SQS Queue
    print("Fetching messages from SQS Queue...")
    messages = etl_process_object.get_messages()

    # Transform IIPs from the messages
    print("Masking PIIs from the messages...")
    message_list = etl_process_object.transform_data(messages)

    # Load data to Postgres
    print("Loading messages to Postgres...")
    etl_process_object.load_data_postgre(message_list)

    # Return from the main function
    return


# Calling the main function
if __name__ == "__main__":
    main()
