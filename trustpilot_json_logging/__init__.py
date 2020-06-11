import sys
import json
import logging
from trustpilot_json_logging import jsonlogger


class JSONFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(JSONFormatter, self).add_fields(log_record, record, message_dict)
        log_record["Module"] = record.name
        log_record["Severity"] = record.levelname


def setup_logging(level="INFO", output=sys.stdout, ignore=None):
    """
    Removes all existing log_handlers and sets up json logger

    :param level: logging level
    :param output: output device, default=sys.stdout
    :param ignore: dict describing thirdparty loggers and their desired level
    
    :Example:

    setup_logging("INFO", sys.stderr, ignore={"elasticsearch":"WARNING"})
    """
    ignore = ignore or {}

    logger = logging.getLogger()
    for h in logger.handlers:
        logger.removeHandler(h)

    log_handler = logging.StreamHandler(output)
    log_handler.setFormatter(JSONFormatter())

    logger.setLevel(level)
    logger.addHandler(log_handler)

    for path, level in ignore.items():
        logging.getLogger(path).setLevel(level)

    logging.info(
        f"Setup logging with level:{level}, ignore: [{', '.join('{}={}'.format(*item) for item in ignore.items())}]"
    )
    return logging
