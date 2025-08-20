import re
import logging
from collections import defaultdict
from .config import CLASHES_FILE # Import the file path

# --- FIX ---
# The 'timings' argument has been removed from the function definition
# to match how it's being called in analysis.py.
def get_clashes(file=CLASHES_FILE) -> dict:
    """
    Reads pre-computed course clashes from a text file.
    """
    clashes = defaultdict(set)

    def parse_ls_code(ls_code: str):
        """Helper to convert 'FC-XXXX-Y' string to ('FC-XXXX', Y) tuple."""
        parts = ls_code.split('-')
        return '-'.join(parts[:2]), int(parts[2])

    try:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                course_codes_str = re.findall(r"\'(.*?)\'", line)
                if not course_codes_str:
                    continue

                clash_group = [parse_ls_code(code) for code in course_codes_str]

                for i in range(len(clash_group)):
                    for j in range(i + 1, len(clash_group)):
                        s1 = clash_group[i]
                        s2 = clash_group[j]
                        clashes[s1].add(s2)
                        clashes[s2].add(s1)

    except FileNotFoundError:
        logging.warning(f"Clash file not found at '{file}'. No clashes will be considered.")
        return {}
    except Exception as e:
        logging.error(f"An error occurred while reading the clash file: {e}")
        return {}

    return dict(clashes)
