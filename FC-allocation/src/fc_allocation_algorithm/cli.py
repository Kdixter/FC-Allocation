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
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # Load data using the simplified, updated functions
    logging.info("Loading course and preference data...")
    timings, capacities, course_info = load_course_data()
    prefs = load_student_preferences()
    taken = load_already_taken() # This will be empty

    # Solve the optimization problem
    logging.info("Starting optimization...")
    assignments, students = solve(timings, capacities, prefs, taken)
    
    if assignments is None:
        logging.error("Optimization failed. No valid assignment found.")
        return

    # Write results and show stats
    logging.info("Writing assignments to output file...")
    write_assignments(args.output, assignments, course_info, students)
    
    stats = assignment_stats(assignments, prefs, taken)
    logging.info("--- Allocation Summary ---")
    logging.info(f"Eligible Students: {stats['eligible_students']}")
    logging.info(f"Total New Courses Assigned: {stats['total_new_courses_assigned']}")
    logging.info(f"Average Preference Weight per Assignment: {stats['avg_weight_per_new_assignment']:.2f}")
    logging.info(f"Total Clashes in New Assignments: {stats['total_clashes_found_new']}")
    logging.info("--------------------------")


if __name__ == "__main__":
    main()
