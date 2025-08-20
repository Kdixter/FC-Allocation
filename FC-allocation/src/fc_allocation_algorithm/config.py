import logging
from pathlib import Path

# --- Basic Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('output/fc_optimize.log'),
    ]
)

# --- File Path Definitions ---
DATA_DIR = Path(__file__).parent.parent.parent / "data"

RANKED_PREFERENCES_FILE = DATA_DIR / "ranked_output.csv"
# Updated to point to the correct capacity file name
COURSE_CAPS_FILE = DATA_DIR / "LS_Caps.csv"
CLASHES_FILE = DATA_DIR / "clashes.txt"

# --- Algorithm Parameters ---
MAX_COURSES = 4
