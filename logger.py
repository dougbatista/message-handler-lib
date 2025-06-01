# message_handler_lib/logger.py
import logging

logger = logging.getLogger("message_handler")

formatter = logging.Formatter(
  fmt="[%(levelname)s] %(name)s.%(funcName)s:%(lineno)d - %(message)s"
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
