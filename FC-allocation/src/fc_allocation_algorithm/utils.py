import re
from collections import defaultdict
from .config import CLASHES_FILE # Import the file path

def get_clashes(timings: dict, file=CLASHES_FILE) -> dict:
    """
    Reads pre-computed course clashes from a text file.

    This function parses a file where each line represents a group of clashing
    courses, for example:
    Clash 1: ['FC-0201-3', 'FC-0306-6']

    It builds a dictionary mapping each course section to a set of sections
    it clashes with.

    Args:
        timings (dict): This argument is kept for compatibility with the original
                        function signature but is no longer used.
        file (str): The path to the clashes text file.

    Returns:
        dict: A dictionary where keys are (course, section) tuples and values
              are sets of other (course, section) tuples they clash with.
    """
    clashes = defaultdict(set)

    def parse_ls_code(ls_code: str):
        """Helper to convert 'FC-XXXX-Y' string to ('FC-XXXX', Y) tuple."""
        parts = ls_code.split('-')
        return '-'.join(parts[:2]), int(parts[2])

    try:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                # Use regex to find all course codes within the single quotes
                course_codes_str = re.findall(r"\'(.*?)\'", line)
                if not course_codes_str:
                    continue

                # Parse the string course codes into the (code, section) tuple format
                clash_group = [parse_ls_code(code) for code in course_codes_str]

                # For each course in the group, add all other courses as clashes
                # This ensures the relationship is reciprocal (if A clashes with B, B clashes with A)
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
