import csv
import re
from collections import defaultdict, Counter
from typing import List, Tuple, Dict
from .config import LS_DETAIL_FILE, PREFERENCES_FILE, ALREADY_TAKEN_FILE, WEIGHTS

def parse_ls_code(ls_code: str) -> Tuple[str, int]:
    parts = ls_code.split('-')
    return '-'.join(parts[:2]), int(parts[2])

def parse_timing(timing_str: str) -> List[Tuple[str, str, str]]:
    timings = []
    for part in timing_str.split(', '):
        m = re.match(r'(\w+)-\((\d{2}:\d{2})-(\d{2}:\d{2})\)', part.strip())
        if m:
            timings.append(m.groups())
    return timings

def load_course_data(file=LS_DETAIL_FILE) -> Tuple[Dict, Dict, Dict]:
    timings, capacities, ls_code_map = {}, {}, {}
    with open(file, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            code, section = parse_ls_code(row['LSCode'])
            timings[(code, section)] = parse_timing(row['TimingsForLS'])
            capacities[(code, section)] = int(row['Availability'])
            ls_code_map[(code, section)] = row['LSCode']
    return timings, capacities, ls_code_map

def load_student_preferences(file=PREFERENCES_FILE) -> Dict:
    prefs = {}
    with open(file, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            rank = int(row['Course Rank'])
            if rank > max(WEIGHTS.keys()):
                continue
            sid = row['StudentId']
            code = row['CourseCode']
            _, sec = parse_ls_code(row['LSCode'])
            prefs[(sid, code, sec)] = WEIGHTS.get(rank, 0)
    return prefs

def load_already_taken(file=ALREADY_TAKEN_FILE) -> Dict:
    taken = defaultdict(list)
    with open(file, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            sid = row['StudentId']
            code, sec = parse_ls_code(row['LSCode'])
            taken[sid].append((code, sec))
    return dict(taken)

def write_assignments(output_file, assignments, ls_code_map, students):
    import csv
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Student', 'Course-1', 'Course-2', 'Course-3', 'Course-4'])
        for sid in sorted(students):
            courses = assignments.get(sid, [])
            row = []
            for sec in courses[:4]:
                ls_code = ls_code_map.get((sec), '')
                row.append(f"{ls_code}")
            row += [''] * (4 - len(row))
            w.writerow([sid] + row)