from core.handler import MessageHandler
from parsers.sqs_parser import SQSParser
from sources.sqs_consumer import SqsConsumer


def process_message(message):
  return True


def run():
  parser = SQSParser()
  handler = MessageHandler(parser, processor=process_message)

  # Replace with your actual SQS queue URL
  sqs_consumer = SqsConsumer(
    queue_url="YOUR_QUEUE_URL HERE", number_of_messages=10, handler=handler
  )

  sqs_consumer.poll_sqs()


if __name__ == "__main__":
  run()
