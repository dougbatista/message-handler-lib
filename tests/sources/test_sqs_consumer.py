from unittest.mock import Mock, call, patch

import pytest

from core.handler import MessageHandler
from sources.sqs_consumer import SqsConsumer


@pytest.fixture
def sqs_consumer(mock_handler):
  with patch("boto3.client") as mock_client:
    client = Mock()
    mock_client.return_value = client
    consumer = SqsConsumer(
      queue_url="http://test-queue",
      number_of_messages=10,
      handler=mock_handler,
    )
    consumer.sqs = mock_client.return_value
    yield consumer


@pytest.fixture
def mock_handler():
  return Mock(spec=MessageHandler)


def test_poll_sqs_processes_messages(sqs_consumer, mock_handler):
  # Arrange
  messages = [
    {"Body": '{"test": "message1"}', "ReceiptHandle": "receipt1"},
    {"Body": '{"test": "message2"}', "ReceiptHandle": "receipt2"},
  ]
  sqs_consumer.sqs.receive_message.side_effect = [
    {"Messages": messages},
    Exception("Stop iteration"),
  ]

  # Act
  with pytest.raises(Exception, match="Stop iteration"):
    sqs_consumer.poll_sqs()

  # Assert
  sqs_consumer.sqs.receive_message.assert_called_with(
    QueueUrl="http://test-queue", MaxNumberOfMessages=10
  )
  assert mock_handler.handle.call_count == 2
  mock_handler.handle.assert_has_calls(
    [call('{"test": "message1"}'), call('{"test": "message2"}')]
  )
  sqs_consumer.sqs.delete_message.assert_has_calls(
    [
      call(QueueUrl="http://test-queue", ReceiptHandle="receipt1"),
      call(QueueUrl="http://test-queue", ReceiptHandle="receipt2"),
    ]
  )


def test_poll_sqs_handles_empty_response(sqs_consumer, mock_handler):
  # Arrange
  sqs_consumer.sqs.receive_message.side_effect = [
    {"Messages": []},
    Exception("Stop iteration"),
  ]

  # Act
  with pytest.raises(Exception, match="Stop iteration"):
    sqs_consumer.poll_sqs()

  # Assert
  mock_handler.handle.assert_not_called()
  sqs_consumer.sqs.delete_message.assert_not_called()


def test_poll_sqs_handles_message_processing_error(sqs_consumer, mock_handler):
  # Arrange
  messages = [{"Body": '{"test": "message"}', "ReceiptHandle": "receipt1"}]
  sqs_consumer.sqs.receive_message.side_effect = [
    {"Messages": messages},
    Exception("Stop iteration"),
  ]
  mock_handler.handle.side_effect = Exception("Processing error")

  # Act
  with pytest.raises(Exception, match="Stop iteration"):
    sqs_consumer.poll_sqs()

  # Assert
  mock_handler.handle.assert_called_once_with('{"test": "message"}')
  sqs_consumer.sqs.delete_message.assert_not_called()
