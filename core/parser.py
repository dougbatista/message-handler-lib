from abc import ABC, abstractmethod

from models.message import Message


class Parser(ABC):
  @abstractmethod
  def parse(self, raw_message: str) -> Message:
    """
    Parse a raw message string into a Message object.

    Args:
        raw_message (str): The raw message string to parse.

    Returns:
        Message: The parsed Message object.
    """
    pass
