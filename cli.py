import argparse
import logging
from fc_allocation_algorithm.data_processing import (
    load_course_data,
    load_student_preferences,
    load_already_taken,
    write_assignments,
)
from fc_allocation_algorithm.optimiser import solve
from fc_allocation_algorithm.analysis import assignment_stats

def main():
    parser = argparse.ArgumentParser(
        description="Allocate students to course sections based on preferences and constraints."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="output/course_assignments.csv",
        help="Output CSV file for course assignments"
    )
    parser.add_argument(
        "--mode",
        choices=["test", "data"],
        default="data",
        help="Mode: 'test' loads test data, 'data' loads real data"
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    if args.mode == "test":
        timings, capacities, course_info = load_course_data(file="test/LS-detail.csv")
        prefs = load_student_preferences(file="test/preferences.csv")
        taken = load_already_taken(file="test/already-taken.csv")
    else:
        timings, capacities, course_info = load_course_data()
        prefs = load_student_preferences()
        taken = load_already_taken()

    assignments, students = solve(timings, capacities, prefs, taken)
    if assignments is None:
        logging.error("No valid assignment found.")
        return

    write_assignments(args.output, assignments, course_info, students)
    stats = assignment_stats(assignments, prefs, timings, taken)
    logging.info(
        f"Assignments: {stats['total_new_courses_assigned']} new, "
        f"Avg weight: {stats['avg_weight_per_new_assignment']:.2f}, "
        f"Clashes: {stats['total_clashes_found_new']}"
    )

if __name__ == "__main__":
    main()