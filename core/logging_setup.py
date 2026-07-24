import logging.config
import yaml
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
LOGGING_CONFIG_PATH = BASE_DIR / "config" / "logging.yaml"
LOGS_DIR = BASE_DIR / "logs"


def setup_logging():
    LOGS_DIR.mkdir(exist_ok=True)
    with LOGGING_CONFIG_PATH.open() as file:
        logging.config.dictConfig(yaml.safe_load(file)) # doc file yaml va chuyen sang python dict
