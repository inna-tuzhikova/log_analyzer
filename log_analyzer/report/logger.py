import logging

from .config import Config


def init_logging(config: Config) -> None:
    logging.basicConfig(
        filename=config.script_log_path,
        format='[%(asctime)s] %(levelname).1s %(message)s',
        datefmt='%Y.%m.%d %H:%M:%S',
        level=logging.INFO
    )
