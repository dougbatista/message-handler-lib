# Message Handler Library

A Python library for handling and processing messages from SQS queues.

## Overview

This library provides a flexible way to handle messages from Amazon SQS (Simple Queue Service) queues with customizable message parsing and processing capabilities.

## Usage

```python
from core.handler import MessageHandler
from parsers.sqs_parser import SQSParser
from sources.sqs_consumer import poll_sqs

# Define your message processing logic
def process_message(message):
  return True

# Initialize parser and handler
parser = SQSParser()
handler = MessageHandler(parser, processor=process_message)

# Start polling messages
poll_sqs(
  queue_url="YOUR_QUEUE_URL",
  number_of_messages=10,
  handler=handler,
)
```

## Components

- `MessageHandler`: Core component that orchestrates message parsing and processing
- `SQSParser`: Parser implementation for SQS messages
- `poll_sqs`: Function to poll messages from an SQS queue

## Configuration

Set your SQS queue URL through environment variables:

```bash
LOCAL_STACK_QUEUE_URL=your-queue-url
```

## Requirements

- Python 3.x
- AWS credentials configured (when using real SQS)
