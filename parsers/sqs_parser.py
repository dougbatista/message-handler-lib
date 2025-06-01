import json
from datetime import datetime
from uuid import uuid4 as uuid

from core.parser import Parser
from logger import logger
from models.message import Message


class SQSParser(Parser):
  """
  A parser implementation for handling SQS messages.

  This parser converts raw JSON messages from Amazon SQS into Message objects.
  It handles missing fields by providing default values and ensures proper
  error handling for malformed messages.

  Attributes:
      None

  Example:
      >>> parser = SQSParser()
      >>> message = parser.parse('{"id": "123", "payload": {"key": "value"}}')
      >>> print(message.id)
      '123'
  """

  def parse(self, raw_message: str) -> Message:
    """
    Parse a raw SQS message string into a Message object.

    Args:
        raw_message (str): A JSON-formatted string containing the message data.
            Expected format: {
                "id": str,          # Optional: UUID will be generated if missing
                "payload": dict,     # Optional: Empty dict if missing
                "timestamp": str     # Optional: Current time if missing
            }

    Returns:
        Message: A Message object containing the parsed data with the following attributes:
            - id: String identifier (UUID if not provided)
            - source: Always "sqs"
            - payload: Dict containing the message payload
            - timestamp: ISO format timestamp string

    Raises:
        ValueError: If the message is not valid JSON or cannot be parsed

    Example:
        >>> raw_msg = '{"id": "123", "payload": {"data": "test"}}'
        >>> message = parser.parse(raw_msg)
        >>> assert message.source == "sqs"
    """
    try:
      data = json.loads(raw_message)
      message = Message(
        id=data.get("id", "{uuid}".format(uuid=uuid())),
        source="sqs",
        payload=data.get("payload", {}),
        timestamp=data.get("timestamp", datetime.now().strftime("%Y-%m-%dT%H:%M:%S")),
      )
      logger.debug(f"Parsed message: {message}")
      return message
    except json.JSONDecodeError as e:
      raise ValueError(f"Invalid JSON format: {e}") from e
    except Exception as e:
      raise ValueError(f"Error parsing message: {e}") from e
