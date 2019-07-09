import logging
import sys
from pathlib import Path

from appdirs import user_data_dir

logger = logging.getLogger(__name__)

DATA_DIR = Path(user_data_dir('snowball', 'dazzler'))
DATABASE_PATH = DATA_DIR / 'db.sqlite3'
CONFIG_PATH = DATA_DIR / 'config.json'


if not DATA_DIR.is_dir():
    try:
        DATA_DIR.mkdir(mode=0o700)
    except OSError:
        logger.critical('Could not create data directory.')
        sys.exit(1)
