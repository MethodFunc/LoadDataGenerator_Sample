import logging
import logging.config
import os
from pathlib import Path
from typing import Optional, List

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATA_TYPE: int
    FREQ: str

    WINDOW_SIZE: Optional[int] = None
    SEQ_LEN: Optional[int] = None

    BATCH_SIZE: Optional[int] = None

    DB_TEST: bool = True
    DB_USER: str
    DB_PWD: str
    DB_HOST: str
    DB_DATABASE: str
    DB_COLLECTION: str
    DB_URI: str

    MODEL_PATH: str
    SCALE_PATH: str
    COLUMNS: Optional[List[str]] = None

    model_config = SettingsConfigDict(env_file=f"{Path(__file__).resolve().parent}/dev.env")


def load_logger(data_type):
    if not os.path.exists('./logs'):
        os.mkdir('./logs')

    log_file = f"./logs/type{data_type}.log"
    logging_config_path = './logging.yaml'
    if os.path.exists(logging_config_path):
        with open(logging_config_path, 'rt') as f:
            logging_config = yaml.load(f, Loader=yaml.FullLoader)
            logging_config['handlers']['file']['filename'] = log_file
            logging.config.dictConfig(logging_config)
    else:
        logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(f"type{data_type}")

    return logger
