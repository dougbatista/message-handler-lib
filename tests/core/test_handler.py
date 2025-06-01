from datetime import datetime
from unittest.mock import Mock

import pytest

from core.handler import MessageHandler
from models.message import Message

MOCKED_DATETIME = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


@pytest.fixture
def mock_parser():
  parser = Mock()
  return parser


@pytest.fixture
def mock_processor():
  processor = Mock()
  return processor


@pytest.fixture
def mock_handler(mock_parser, mock_processor):
  return MessageHandler(parser=mock_parser, processor=mock_processor)


def test_handle_successful_message(mock_handler, mock_parser, mock_processor):
  # Arrange
  raw_message = '{"id": "123", "payload": {"test": "data"}}'
  expected_parsed = Message(
    id="123", source="sqs", payload={"test": "data"}, timestamp=MOCKED_DATETIME
  )
  mock_parser.parse.return_value = expected_parsed

  # Act
  mock_handler.handle(raw_message)

  # Assert
  mock_parser.parse.assert_called_once_with(raw_message)
  mock_processor.assert_called_once_with(expected_parsed)


def test_handle_parser_error(mock_handler, mock_parser):
  # Arrange
  raw_message = "invalid message"
  mock_parser.parse.side_effect = ValueError("Invalid message format")

  # Act & Assert
  with pytest.raises(ValueError) as exc_info:
    mock_handler.handle(raw_message)

  assert str(exc_info.value) == "Invalid message format"
  mock_parser.parse.assert_called_once_with(raw_message)


def test_handle_processor_error(mock_handler, mock_parser, mock_processor):
  # Arrange
  raw_message = '{"id": "123"}'
  parsed_message = Message(
    id="123", source="sqs", payload={}, timestamp=MOCKED_DATETIME
  )
  mock_parser.parse.return_value = parsed_message
  mock_processor.side_effect = Exception("Processing failed")

  # Act & Assert
  with pytest.raises(Exception) as exc_info:
    mock_handler.handle(raw_message)

  assert str(exc_info.value) == "Processing failed"
  mock_parser.parse.assert_called_once_with(raw_message)
  mock_processor.assert_called_once_with(parsed_message)
