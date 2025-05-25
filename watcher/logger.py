import logging

from os.path import expanduser


def setup_logger(log_path: str) -> None:
    full_path = expanduser(log_path)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(full_path),
            logging.StreamHandler()
        ]
    )