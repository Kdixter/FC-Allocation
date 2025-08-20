from typing import Dict, List, Tuple
from collections import defaultdict

def assignment_stats(
    assignments: Dict[str, List[Tuple[str, str]]],
    prefs: Dict[Tuple[str, str, str], int],
    timings: Dict,
    already_taken: Dict[str, List[Tuple[str, str]]]
) -> Dict[str, float]:
    """
    Compute totals and weights for NEW assignments only (ignores preassigned courses).

    Returns a dict with:
      - total_students (int)
      - already_taken_students (int)
      - eligible_students (int)
      - students_with_new_assignments (int)
      - students_with_pref_new (int)    # students who got >=1 preferred new course (weight>0)
      - students_without_pref_new (int) # students who got new assignments but no preferred ones
      - total_new_courses_assigned (int)
      - total_pref_weight_assigned_new (int)
      - avg_weight_per_new_assignment (float)            # weight sum / total_new_courses_assigned
      - avg_weight_per_eligible_student (float)          # weight sum / eligible_students
      - avg_weight_per_student_with_new_assignments (float)
      - total_clashes_found_new (int)
    """
    from .utils import get_clashes

    clashes = get_clashes(timings)

    total_students = len(assignments)
    already_taken_students = sum(1 for sid in assignments if already_taken.get(sid))
    eligible_students = total_students - already_taken_students

    total_new_courses_assigned = 0
    total_pref_weight_assigned_new = 0

    students_with_new_assignments = 0
    students_with_pref_new = 0

    total_clashes_found_new = 0

    for sid, assigned_list in assignments.items():
        # treat both assigned_list and already_taken entries as tuples
        preassigned_set = set(already_taken.get(sid, []))
        new_assigned_set = set(assigned_list) - preassigned_set

        if not new_assigned_set:
            continue

        students_with_new_assignments += 1
        # sum weights for this student's new assignments
        weight_sum_student = 0
        for course, section in new_assigned_set:
            weight = prefs.get((sid, course, section), 0)
            weight_sum_student += weight

        total_pref_weight_assigned_new += weight_sum_student
        total_new_courses_assigned += len(new_assigned_set)

        if weight_sum_student > 0:
            students_with_pref_new += 1

        # clash check among new assignments (count each clash once)
        new_assigned_list = list(new_assigned_set)
        for i in range(len(new_assigned_list)):
            sec1 = new_assigned_list[i]
            conflict_set = clashes.get(sec1, set())
            for j in range(i + 1, len(new_assigned_list)):
                if new_assigned_list[j] in conflict_set:
                    total_clashes_found_new += 1

    students_without_pref_new = students_with_new_assignments - students_with_pref_new

    avg_weight_per_new_assignment = (
        total_pref_weight_assigned_new / total_new_courses_assigned
        if total_new_courses_assigned > 0 else 0.0
    )

    avg_weight_per_eligible_student = (
        total_pref_weight_assigned_new / eligible_students
        if eligible_students > 0 else 0.0
    )

    avg_weight_per_student_with_new_assignments = (
        total_pref_weight_assigned_new / students_with_new_assignments
        if students_with_new_assignments > 0 else 0.0
    )

    return {
        "total_students": int(total_students),
        "already_taken_students": int(already_taken_students),
        "eligible_students": int(eligible_students),
        "students_with_new_assignments": int(students_with_new_assignments),
        "students_with_pref_new": int(students_with_pref_new),
        "students_without_pref_new": int(students_without_pref_new),
        "total_new_courses_assigned": int(total_new_courses_assigned),
        "total_pref_weight_assigned_new": int(total_pref_weight_assigned_new),
        "avg_weight_per_new_assignment": float(avg_weight_per_new_assignment),
        "avg_weight_per_eligible_student": float(avg_weight_per_eligible_student),
        "avg_weight_per_student_with_new_assignments": float(avg_weight_per_student_with_new_assignments),
        "total_clashes_found_new": int(total_clashes_found_new),
    }