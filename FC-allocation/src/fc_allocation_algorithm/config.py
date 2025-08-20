import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('output/fc_optimize.log'),
    ]
)

from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"

LS_DETAIL_FILE = DATA_DIR / "LS-detail.csv"
PREFERENCES_FILE = DATA_DIR / "preferences.csv"
ALREADY_TAKEN_FILE = DATA_DIR / "already-taken.csv"

WEIGHTS = {
    1: 11,
    2: 9,
    3: 7,
    4: 4, 
    5: 3
}

MAX_COURSES = 4