import logging
from pathlib import Path

# --- Basic Logging Configuration ---
# Sets up logging to both the console and a file in the output directory.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('output/fc_optimize.log'),
    ]
)

# --- File Path Definitions ---
# Defines the default location for input data files.
DATA_DIR = Path(__file__).parent.parent.parent / "data"

# The ranked preferences file is the primary input for student choices.
RANKED_PREFERENCES_FILE = DATA_DIR / "ranked_output.csv"
# The new file containing the actual capacity for each course section.
COURSE_CAPS_FILE = DATA_DIR / "FC Preference Real Data - LS Caps.csv"
# Path for the pre-computed clash file.
CLASHES_FILE = DATA_DIR / "clashes.txt"

# --- Algorithm Parameters ---
# The maximum number of courses a student should be assigned.
MAX_COURSES = 4
