# Message Handler Library

A Python library for handling and processing messages from SQS queues.

## Overview

This library provides a flexible way to handle messages from Amazon SQS (Simple Queue Service) queues with customizable message parsing and processing capabilities.

## Usage SQS Consumer

```python
from core.handler import MessageHandler
from parsers.sqs_parser import SQSParser
from sources.sqs_consumer import SqsConsumer

def message_processor(message):
  print(message)

def run():
  parser = SQSParser()
  handler = MessageHandler(parser, processor=message_processor)

  sqs_consumer = SqsConsumer(
    queue_url="YOUR_QUEUE", number_of_messages=10, handler=handler
  )

  sqs_consumer.poll_sqs()

run()
```

## Usage SQS Producer

```python

from sources.sqs_producer import SqsProducer

def run():
  sqs_producer = SqsProducer(
    queue_url="http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/localstack-queue-output"
  )

  message_id = sqs_producer.send_message(message_body=str(message))

  print(f"Message processed and sent with ID: {message_id}")

run()
```

## Components

- `MessageHandler`: Core component that orchestrates message parsing and processing
- `SQSParser`: Parser implementation for SQS messages
- `poll_sqs`: Function to poll messages from an SQS queue

## Requirements

- Python 3.x
- AWS credentials configured (when using real SQS)
