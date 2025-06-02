from sources.sqs_producer import SqsProducer


def process_message(message):
  print(f"Processing message: {message}")

  sqs_producer = SqsProducer(
    queue_url="YOUR_QUEUE_URL_HERE"  # Replace with your actual SQS queue URL
  )

  message_id = sqs_producer.send_message(message_body=str(message))

  print(f"Message processed and sent with ID: {message_id}")


process_message({"key": "value", "another_key": "another_value"})
