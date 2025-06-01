from unittest.mock import Mock, call, patch

import pytest

from core.handler import MessageHandler
from sources.sqs_consumer import poll_sqs


@pytest.fixture
def mock_sqs_client():
  with patch("boto3.client") as mock_client:
    client = Mock()
    mock_client.return_value = client
    yield client


@pytest.fixture
def mock_handler():
  return Mock(spec=MessageHandler)


def test_poll_sqs_processes_messages(mock_sqs_client, mock_handler):
  # Arrange
  queue_url = "http://test-queue"
  messages = [
    {"Body": '{"test": "message1"}', "ReceiptHandle": "receipt1"},
    {"Body": '{"test": "message2"}', "ReceiptHandle": "receipt2"},
  ]
  mock_sqs_client.receive_message.side_effect = [
    {"Messages": messages},
    Exception("Stop iteration"),  # To break the infinite loop
  ]

  # Act
  with pytest.raises(Exception, match="Stop iteration"):
    poll_sqs(queue_url, 10, mock_handler)

  # Assert
  mock_sqs_client.receive_message.assert_called_with(
    QueueUrl=queue_url, MaxNumberOfMessages=10
  )
  assert mock_handler.handle.call_count == 2
  mock_handler.handle.assert_has_calls(
    [call('{"test": "message1"}'), call('{"test": "message2"}')]
  )
  mock_sqs_client.delete_message.assert_has_calls(
    [
      call(QueueUrl=queue_url, ReceiptHandle="receipt1"),
      call(QueueUrl=queue_url, ReceiptHandle="receipt2"),
    ]
  )


def test_poll_sqs_handles_empty_response(mock_sqs_client, mock_handler):
  # Arrange
  queue_url = "http://test-queue"
  mock_sqs_client.receive_message.side_effect = [
    {"Messages": []},
    Exception("Stop iteration"),
  ]

  # Act
  with pytest.raises(Exception, match="Stop iteration"):
    poll_sqs(queue_url, 10, mock_handler)

  # Assert
  mock_handler.handle.assert_not_called()
  mock_sqs_client.delete_message.assert_not_called()


def test_poll_sqs_handles_message_processing_error(mock_sqs_client, mock_handler):
  # Arrange
  queue_url = "http://test-queue"
  messages = [{"Body": '{"test": "message"}', "ReceiptHandle": "receipt1"}]
  mock_sqs_client.receive_message.side_effect = [
    {"Messages": messages},
    Exception("Stop iteration"),
  ]
  mock_handler.handle.side_effect = Exception("Processing error")

  # Act
  with pytest.raises(Exception, match="Stop iteration"):
    poll_sqs(queue_url, 10, mock_handler)

  # Assert
  mock_handler.handle.assert_called_once_with('{"test": "message"}')
  mock_sqs_client.delete_message.assert_not_called()
