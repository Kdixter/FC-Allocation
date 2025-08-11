from z3 import Optimize, Bool, Implies, Or, If, Sum, PbLe, Not, And, is_true, sat, unsat
from collections import defaultdict
from typing import Dict
from .utils import get_clashes
from .config import MAX_COURSES
import logging

logger = logging.getLogger(__name__)

def create_model(timings: Dict, capacities: Dict, prefs: Dict, taken: Dict):
    opt = Optimize()
    students = set(sid for sid, *_ in prefs.keys()) | set(taken.keys())
    all_courses = set(code for _, code, _ in prefs.keys())

    clashes = get_clashes(timings)
    course_vars, section_vars = {}, {}

    for sid in students:
        taken_courses = {t[0] for t in taken.get(sid, [])}
        taken_sections = taken.get(sid, [])

        for code in all_courses:
            if code in taken_courses:
                continue
            pref_sections = [sec for (s, c, sec) in prefs if s == sid and c == code]
            feasible_sections = [
                sec for sec in pref_sections
                if capacities.get((code, sec), 0) > 0
                and not any(sec in clashes.get(t_sec, set()) for t_sec in taken_sections)
            ]
            if not feasible_sections:
                continue
            cvar = Bool(f"course_{sid}_{code}")
            course_vars[(sid, code)] = cvar
            sec_vars_for_course = []
            for sec in feasible_sections:
                svar = Bool(f"section_{sid}_{code}_{sec}")
                section_vars[(sid, code, sec)] = svar
                opt.add(Implies(svar, cvar))
                sec_vars_for_course.append(svar)
            opt.add(cvar == Or(sec_vars_for_course))

    weights = [
        If(cvar, max([rank for (s, c, sec), rank in prefs.items() if s == sid and c == code]), 0)
        for (sid, code), cvar in course_vars.items()
    ]
    if weights:
        opt.maximize(Sum(weights))

    for sid in students:
        taken_count = len(taken.get(sid, []))
        max_new = max(0, MAX_COURSES - taken_count)
        cvars = [cvar for (s, c), cvar in course_vars.items() if s == sid]
        if max_new == 0:
            for cvar in cvars:
                opt.add(cvar == False)
        elif cvars:
            opt.add(Sum([If(cvar, 1, 0) for cvar in cvars]) + taken_count == MAX_COURSES)

    sec_assigns = defaultdict(list)
    for (sid, code, sec), svar in section_vars.items():
        sec_assigns[(code, sec)].append(svar)
    for sec_key, vlist in sec_assigns.items():
        cap = capacities.get(sec_key, 0)
        if cap <= 0:
            for v in vlist:
                opt.add(v == False)
        else:
            opt.add(PbLe([(v, 1) for v in vlist], cap))

    for sid in students:
        s_sections = [((c, sec), v) for (s, c, sec), v in section_vars.items() if s == sid]
        for i, (sec1, v1) in enumerate(s_sections):
            clash_with_sec1 = clashes.get(sec1, set())
            for sec2, v2 in s_sections[i+1:]:
                if sec2 in clash_with_sec1:
                    opt.add(Not(And(v1, v2)))
        for t_sec in taken.get(sid, []):
            clash_with_tsec = clashes.get(t_sec, set())
            for sec, v in s_sections:
                if sec in clash_with_tsec:
                    opt.add(v == False)

    return opt, course_vars, section_vars, students

def solve(timings, capacities, prefs, taken):
    opt, _, section_vars, students = create_model(timings, capacities, prefs, taken)
    res = opt.check()
    if res == sat:
        model = opt.model()
        assignments = defaultdict(list)
        for (sid, code, sec), svar in section_vars.items():
            if is_true(model.evaluate(svar)):
                assignments[sid].append((code, sec))
        for sid, courses in taken.items():
            for c, sec in courses:
                if (c, sec) not in assignments[sid]:
                    assignments[sid].append((c, sec))
        for sid in assignments:
            assignments[sid].sort()
        logger.info(f"Solution found. Total assignments: {sum(len(cs) for cs in assignments.values())}")
        return assignments, students
    logger.warning("No solution found." if res == unsat else f"Unexpected solver result: {res}")
    return None, None