# message_handler_lib/sources/sqs_producer.py
import json

import boto3
from botocore.exceptions import ClientError

from logger import logger


class SqsProducer:
  def __init__(self, queue_url: str):
    self.queue_url = queue_url
    self.client = boto3.client("sqs")

  def send_message(
    self, message_body: dict, message_group_id: str = None, deduplication_id: str = None
  ):
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
