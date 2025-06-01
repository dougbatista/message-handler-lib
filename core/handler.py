from logger import logger


class MessageHandler:
  """
  A class that handles message processing by combining a parser and processor.

  The MessageHandler coordinates the parsing and processing of messages by using
  a provided parser to convert raw messages into Message objects and a processor
  to handle the parsed messages.

  Attributes:
      parser: An object implementing a parse(raw_message) method.
      processor: A callable that processes parsed Message objects.

  Example:
      >>> parser = SQSParser()
      >>> processor = lambda msg: print(msg)
      >>> handler = MessageHandler(parser, processor)
      >>> handler.handle('{"id": "123", "payload": {}}')
  """

  def __init__(self, parser, processor):
    """
    Initialize a new MessageHandler instance.

    Args:
        parser: An object with a parse(raw_message) method that converts raw messages
               into Message objects.
        processor: A callable that takes a Message object as input and processes it.

    Raises:
        TypeError: If parser or processor are not of the correct type.
    """
    self.parser = parser
    self.processor = processor

  def handle(self, raw_message):
    """
    Process a raw message using the configured parser and processor.

    This method attempts to parse the raw message using the parser and then
    processes the resulting Message object using the processor. All exceptions
    are logged and re-raised.

    Args:
        raw_message: A string containing the raw message to be processed.

    Raises:
        Exception: Any exception that occurs during parsing or processing is
                  logged and re-raised.

    Returns:
        None
    """
    try:
      parsed = self.parser.parse(raw_message)
      self.processor(parsed)
      logger.info(f"Message processed successfully: {parsed}")
    except Exception as e:
      logger.exception(f"Error processing message: {e}")
      raise
