import logging

from loguru import logger


def setup_logging(level: int = logging.INFO) -> None:
    logger.remove()
    logger.add(
        lambda msg: logging.getLogger().handle(
            logging.LogRecord("loguru", level, __file__, 0, msg, None, None)
        )
    )
