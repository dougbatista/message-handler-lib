from typing import Any, Dict, Literal

from pydantic import BaseModel


class Message(BaseModel):
  id: str
  source: Literal["kafka", "sqs", "http"]
  payload: Dict[str, Any]
  timestamp: str


# class MessageResponse(BaseModel):
