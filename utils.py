import string
import logging
import random

NUM_AUDIOS = 100

AUDIO_DELAY = 1
TRANSCRIBE_DELAY = 5
CLASSIFY_DELAY = 2

NUM_AUDIO_THREADS = 5
NUM_TRANSCRIBE_THREADS = 2
NUM_CLASSIFY_THREADS = 4


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def classify():
    return random.choice(["client", "agent"])


# Configure the logger
# logging.basicConfig(
#     level=logging.DEBUG,  # Set the logging level (you can change this to INFO, WARNING, ERROR, or CRITICAL)
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     # filename='mylog.log',  # Set the log file's name
#     # filemode='w'  # Use 'w' to overwrite the log file on each run, 'a' to append
# )


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())
logger = logging.getLogger("Logger")
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

with open("database.txt", "w") as f:
    pass
