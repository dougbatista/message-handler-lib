import os

import boto3
from botocore.config import Config

from core.handler import MessageHandler
from logger import logger


class SqsConsumer:
  def __init__(self, queue_url: str, number_of_messages: int, handler: MessageHandler):
    """
    Initializes the SqsConsumer with the specified queue URL, number of messages to poll,
    and a message handler.

    Args:
        queue_url (str): The URL of the SQS queue to poll.
        number_of_messages (int): Maximum number of messages to receive in each polling request.
            If None or 0, defaults to 100 messages.
        handler (MessageHandler): Instance of MessageHandler to process received messages.
    """
    self.queue_url = queue_url
    self.number_of_messages = number_of_messages
    self.handler = handler
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

  def poll_sqs(self):
    """
    Continuously polls an SQS queue for messages and processes them using the provided handler.

    This function runs indefinitely, polling the specified SQS queue for messages.
    When messages are received, they are processed using the provided MessageHandler
    and then deleted from the queue upon successful processing.

    Args:
        None
    Raises:
        boto3.exceptions.Boto3Error: For AWS/SQS-related errors
        Exception: For message processing errors (logged but not re-raised)

    Example:
        >>> handler = MessageHandler(SQSParser(), message_processor)
        >>> poll_sqs()
    """
    logger.info(
      f"Polling SQS queue: {self.queue_url} for {self.number_of_messages} messages"
    )
    while True:
      response = self.client.receive_message(
        QueueUrl=self.queue_url, MaxNumberOfMessages=self.number_of_messages or 100
      )

      messages = response.get("Messages", [])

      if not messages:
        continue

      for message in messages:
        try:
          self.handler.handle(message["Body"])
          self.client.delete_message(
            QueueUrl=self.queue_url, ReceiptHandle=message["ReceiptHandle"]
          )
        except Exception as e:
          logger.error(f"Error processing message: {e}")
          logger.error(f"Failed message: {message['Body']}")
