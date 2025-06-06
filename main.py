import os

from core.handler import MessageHandler
from parsers.sqs_parser import SQSParser
from sources.sqs_consumer import SqsConsumer
from sources.sqs_producer import SqsProducer


def process_message(message):
  print(f"Processing message: {message}")

  sqs_producer = SqsProducer(
    queue_url="http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/localstack-queue-output"
  )

  message_id = sqs_producer.send_message(message_body=str(message))

  print(f"Message processed and sent with ID: {message_id}")

  return True


def run():
  parser = SQSParser()
  handler = MessageHandler(parser, processor=process_message)

  sqs_consumer = SqsConsumer(
    queue_url=os.getenv("LOCAL_STACK_QUEUE_URL"), number_of_messages=10, handler=handler
  )

  sqs_consumer.poll_sqs()


if __name__ == "__main__":
  run()
