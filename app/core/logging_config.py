import logging
import sys

from colorlog import ColoredFormatter


def configure_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if root_logger.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)

    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    logging.getLogger("app").setLevel(logging.INFO)
    # if not root_logger.handlers:
    #     logging.basicConfig(
    #         level=logging.INFO,
    #         format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    #     )
    # logging.getLogger("app").setLevel(logging.INFO)
