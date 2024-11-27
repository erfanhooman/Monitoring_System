import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = "local_ms.log"

LOG_LEVEL = logging.INFO

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3),
        logging.StreamHandler(),  # Logs to console
    ],
)

def get_logger(name: str):
    """Return a logger for the given module name."""
    return logging.getLogger(name)