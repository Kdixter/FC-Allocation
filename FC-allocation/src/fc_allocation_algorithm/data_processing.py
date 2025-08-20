import csv
import re
import logging
from collections import defaultdict
from typing import List, Tuple, Dict
from .config import RANKED_PREFERENCES_FILE, COURSE_CAPS_FILE, MAX_COURSES

def parse_ls_code(ls_code: str) -> Tuple[str, int]:
    """Parses an LSCode string like 'FC-0102-1' into ('FC-0102', 1)."""
    try:
        parts = ls_code.split('-')
        return '-'.join(parts[:2]), int(parts[2])
    except (IndexError, ValueError):
        logging.warning(f"Could not parse LSCode: {ls_code}")
        return None, None

def load_course_data(prefs_file=RANKED_PREFERENCES_FILE, caps_file=COURSE_CAPS_FILE) -> Tuple[Dict, Dict, Dict]:
    """
    Loads course data by reading capacities from the official caps file and
    discovering all unique courses from the student preferences file.
    """
    capacities, ls_code_map = {}, {}
    
    official_caps = {}
    try:
        with open(caps_file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            
            ls_code_header = next((h for h in headers if h.replace(" ", "").lower() in ['lscode', 'fccode']), None)
            # --- FIX: Added 'adjustedcap' to the list of possible capacity column names ---
            capacity_header = next((h for h in headers if h.replace(" ", "").lower() in ['capacity', 'caps', 'availability', 'adjustedcap']), None)

            if not ls_code_header or not capacity_header:
                logging.error(f"CRITICAL: Could not find 'LSCode'/'FC Code' or a valid Capacity column in '{caps_file}'.")
                return {}, {}, {}

            for row in reader:
                ls_code = row.get(ls_code_header)
                capacity_val = row.get(capacity_header)
                if ls_code and capacity_val is not None:
                    official_caps[ls_code] = int(capacity_val)

    except FileNotFoundError:
        logging.error(f"CRITICAL: Course capacity file not found at '{caps_file}'. Cannot proceed.")
        return {}, {}, {}
    except (ValueError, KeyError) as e:
        logging.error(f"Error reading capacity file. Check column names and values. Details: {e}")
        return {}, {}, {}

    unique_ls_codes = set()
    try:
        with open(prefs_file, encoding='utf-8') as f:
            for row in csv.DictReader(f):
                if 'LSCode' in row:
                    unique_ls_codes.add(row['LSCode'])
    except FileNotFoundError:
        logging.error(f"Preferences file not found: {prefs_file}")
        return {}, {}, {}

    for ls_code in unique_ls_codes:
        code, section = parse_ls_code(ls_code)
        if code:
            capacity = official_caps.get(ls_code, 0)
            if capacity == 0:
                logging.warning(f"Course {ls_code} from preferences not found in capacity file or has 0 capacity.")
            
            capacities[(code, section)] = capacity
            ls_code_map[(code, section)] = ls_code
            
    timings = {}
    return timings, capacities, ls_code_map

def load_student_preferences(file=RANKED_PREFERENCES_FILE) -> Dict:
    """
    Loads student preferences from the pre-processed ranked_output.csv file.
    """
    prefs = {}
    try:
        with open(file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    weight = int(row['weight'])
                    sid = row['StudentId']
                    ls_code = row['LSCode']
                    code, sec = parse_ls_code(ls_code)
                    if code:
                        prefs[(sid, code, sec)] = weight
                except (KeyError, ValueError) as e:
                    logging.warning(f"Skipping preference row due to error: {row}. Details: {e}")
                    continue
    except FileNotFoundError:
        logging.error(f"Preferences file not found: {file}")
    return prefs

def load_already_taken() -> Dict:
    """
    Returns an empty dictionary as pre-assignments are no longer provided.
    """
    return {}

def write_assignments(output_file, assignments, ls_code_map, students):
    """Writes the final student course assignments to a CSV file."""
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['Student', 'Course-1', 'Course-2', 'Course-3', 'Course-4'])
            for sid in sorted(students):
                courses = assignments.get(sid, [])
                row = [ls_code_map.get(sec_tuple, '') for sec_tuple in courses[:MAX_COURSES]]
                row += [''] * (MAX_COURSES - len(row))
                w.writerow([sid] + row)
        logging.info(f"Successfully wrote assignments to {output_file}")
    except Exception as e:
        logging.error(f"Failed to write assignments to file: {e}")
