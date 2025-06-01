from core.handler import MessageHandler
from parsers.sqs_parser import SQSParser
from sources.sqs_consumer import poll_sqs


def process_message(message):
  return True


def run():
  parser = SQSParser()
  handler = MessageHandler(parser, processor=process_message)

  poll_sqs(
    queue_url="MY_SQS_QUEUE_URL",
    number_of_messages=10,
    handler=handler,
  )


if __name__ == "__main__":
  run()
