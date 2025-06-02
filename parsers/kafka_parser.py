import json
from datetime import datetime
from uuid import uuid4 as uuid

from core.parser import Parser
from logger import logger
from models.message import Message


class KafkaParser(Parser):
  def parse(self, raw_message: str) -> Message:
    try:
      data = json.loads(raw_message)
      message = Message(
        id=data.get("id", "{uuid}".format(uuid=uuid())),
        source="kafka",
        payload=data.get("payload", {}),
        timestamp=data.get("timestamp", datetime.now().strftime("%Y-%m-%dT%H:%M:%S")),
      )
      logger.debug(f"Parsed message: {message}")
      return message
    except json.JSONDecodeError as e:
      raise ValueError(f"Invalid JSON format: {e}") from e
    except Exception as e:
      raise ValueError(f"Error parsing message: {e}") from e
