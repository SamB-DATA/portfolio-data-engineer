import logging
import logging.config
from pathlib import Path

import yaml


BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOGGING_CONFIG_PATH = BASE_DIR / "config" / "logging.yaml"


def setup_logging():

    if LOGGING_CONFIG_PATH.exists():

        with open(LOGGING_CONFIG_PATH, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        logging.config.dictConfig(config)

    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )


def get_logger(name: str):

    setup_logging()

    return logging.getLogger(name)