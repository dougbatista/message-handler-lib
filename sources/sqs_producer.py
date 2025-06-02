# message_handler_lib/sources/sqs_producer.py
import json
import os

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from logger import logger


class SqsProducer:
  def __init__(self, queue_url: str):
    """
    Initialize the SqsProducer with the specified SQS queue URL.
    Args:
      queue_url (str): The URL of the SQS queue to which messages will be sent.
    """
    self.queue_url = queue_url
    # self.client = boto3.client("sqs")
    self.client = boto3.client(
      "sqs",
      region_name=os.getenv("LOCAL_STACK_REGION"),
      endpoint_url=os.getenv("LOCAL_STACK_URL"),
      aws_access_key_id=os.getenv("LOCAL_STACK_ACCESS_KEY_ID"),
      aws_secret_access_key=os.getenv("LOCAL_STACK_ACCESS_KEY_ID"),
      use_ssl=False,
      verify=False,
      aws_session_token=None,
      config=Config(retries=dict(max_attempts=3)),
    )

  def send_message(
    self, message_body: dict, message_group_id: str = None, deduplication_id: str = None
  ):
    """
    Send a message to the specified SQS queue.
    Args:
      message_body (dict): The message body to send, which will be converted to JSON.
      message_group_id (str, optional): The message group ID for FIFO queues.
      deduplication_id (str, optional): The deduplication ID for FIFO queues.
    Returns:
      str: The ID of the sent message.
    Raises:
      ClientError: If there is an error sending the message to SQS.
    """
    try:
      params = {
        "QueueUrl": self.queue_url,
        "MessageBody": json.dumps(message_body),
      }

      # For FIFO queues
      if message_group_id:
        params["MessageGroupId"] = message_group_id
      if deduplication_id:
        params["MessageDeduplicationId"] = deduplication_id

      response = self.client.send_message(**params)
      logger.info(f"Message sent to SQS: {response['MessageId']}")
      return response["MessageId"]

    except ClientError as e:
      logger.error(f"Failed to send message to SQS: {e}")
      raise
