from unittest.mock import patch

import pytest
from botocore.exceptions import ClientError

from sources.sqs_producer import SqsProducer


@pytest.fixture
def sqs_producer():
  with patch("boto3.client") as mock_client:
    producer = SqsProducer(queue_url="http://test-queue")
    producer.client = mock_client.return_value
    yield producer


def test_send_message_successfully(sqs_producer):
  # Arrange
  message_body = {"test": "message"}
  expected_message_id = "test-message-id"
  sqs_producer.client.send_message.return_value = {"MessageId": expected_message_id}

  # Act
  message_id = sqs_producer.send_message(message_body)

  # Assert
  assert message_id == expected_message_id
  sqs_producer.client.send_message.assert_called_once_with(
    QueueUrl="http://test-queue", MessageBody='{"test": "message"}'
  )


def test_send_message_with_fifo_attributes(sqs_producer):
  # Arrange
  message_body = {"test": "message"}
  message_group_id = "test-group"
  deduplication_id = "test-dedup"
  expected_message_id = "test-message-id"
  sqs_producer.client.send_message.return_value = {"MessageId": expected_message_id}

  # Act
  message_id = sqs_producer.send_message(
    message_body, message_group_id=message_group_id, deduplication_id=deduplication_id
  )

  # Assert
  assert message_id == expected_message_id
  sqs_producer.client.send_message.assert_called_once_with(
    QueueUrl="http://test-queue",
    MessageBody='{"test": "message"}',
    MessageGroupId=message_group_id,
    MessageDeduplicationId=deduplication_id,
  )


def test_send_message_handles_client_error(sqs_producer):
  # Arrange
  message_body = {"test": "message"}
  error_message = "Test error message"
  sqs_producer.client.send_message.side_effect = ClientError(
    error_response={"Error": {"Message": error_message}}, operation_name="SendMessage"
  )

  # Act & Assert
  with pytest.raises(ClientError):
    sqs_producer.send_message(message_body)


@pytest.mark.parametrize(
  "message_body",
  [
    {},
    {"key": "value"},
    {"nested": {"key": "value"}},
    {"list": [1, 2, 3]},
  ],
)
def test_send_message_with_different_payloads(sqs_producer, message_body):
  # Arrange
  expected_message_id = "test-message-id"
  sqs_producer.client.send_message.return_value = {"MessageId": expected_message_id}

  # Act
  message_id = sqs_producer.send_message(message_body)

  # Assert
  assert message_id == expected_message_id
  sqs_producer.client.send_message.assert_called_once()
