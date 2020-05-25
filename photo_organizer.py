import argparse
import logging
import datetime
import os

from exception.exception import InvalidInputException, InvalidConfigException
from photo_organizer.config import Config
from photo_organizer.organizer import Organizer

# All supported actions
supported_actions = ["analyze", "setup"]

logging_format = "%(asctime)s %(threadName)s [%(levelname)s] %(message)s"


def setup_console_logging(level):
    """
    Setup console logging and the root logger with level
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level=logging.getLevelName(level))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(logging_format))
    logging.getLogger().addHandler(console_handler)


def setup_file_logging(config, command):
    """
    Setup file logger logging to WorkingDir/Logs/[datetime]_[command].log
    """
    file_name = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{command}.log"
    dir_path = os.path.join(config.working_dir, "Logs")
    os.makedirs(dir_path, exist_ok=True)
    file_handler = logging.FileHandler(os.path.join(dir_path, file_name))
    file_handler.setFormatter(logging.Formatter(logging_format))
    logging.getLogger().addHandler(file_handler)


def parse_args():
    """
    Parse the arguments
    @return: the args
    """
    parser = argparse.ArgumentParser(description='Photo Organizer.')
    parser.add_argument('action', help="setup, X or Y")
    parser.add_argument('-debug', action="store_true", help="enable debug logging")
    return parser.parse_args()


def main():
    """
    Main function for running the commands and handling the results
    """
    args = parse_args()
    setup_console_logging("DEBUG" if args.debug else "INFO")

    if args.action not in supported_actions:
        raise InvalidInputException(f"Unsupported command '{args.action}'")

    config = Config()
    setup_file_logging(config, args.action)
    logging.info(f"Running command {args.action}")

    try:
        organizer = Organizer(config)
        if args.action == "analyze":
            organizer.analyze()
        elif args.action == "setup":
            organizer.setup()
        else:
            raise InvalidInputException(f"Unsupported command '{args.action}'")
    except (InvalidInputException, InvalidConfigException) as ex:
        logging.error(f"{ex.args[0]}")


main()
