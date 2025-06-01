import json

import pytest

from models.message import Message
from parsers.sqs_parser import SQSParser


@pytest.fixture
def parser():
  return SQSParser()


def test_parse_valid_message(parser):
  # Arrange
  test_message = {
    "id": "test-id-123",
    "payload": {"key": "value"},
    "timestamp": "2025-06-01T10:00:00",
  }
  raw_message = json.dumps(test_message)

  # Act
  result = parser.parse(raw_message)

  # Assert
  assert isinstance(result, Message)
  assert result.id == "test-id-123"
  assert result.source == "sqs"
  assert result.payload == {"key": "value"}
  assert result.timestamp == "2025-06-01T10:00:00"


def test_parse_invalid_json(parser):
  # Arrange
  raw_message = "invalid json"

  # Act & Assert
  with pytest.raises(ValueError) as exc_info:
    parser.parse(raw_message)

  assert "Invalid JSON format" in str(exc_info.value)


def test_parse_none_message(parser):
  # Arrange
  raw_message = None

  # Act & Assert
  with pytest.raises(ValueError) as exc_info:
    parser.parse(raw_message)

  assert "Error parsing message" in str(exc_info.value)
