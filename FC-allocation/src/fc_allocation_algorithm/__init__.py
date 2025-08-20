# src/fc_allocation_algorithm/__init__.py

__version__ = "0.1.0"

from .optimiser import (
    create_model,
    solve,
)

from .data_processing import (
    load_course_data,
    load_student_preferences,
    load_already_taken,
)

from .utils import (
    get_clashes,
)

__all__ = [
    "create_optimization_model",
    "solve_and_output_assignments",
    "load_course_data",
    "load_student_preferences",
    "load_already_taken",
    "time_overlap",
]