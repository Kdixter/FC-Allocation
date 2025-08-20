# FC Allocation Algorithm

A Python package for allocating students to FCs based on preferences, capacities, and scheduling constraints using Z3 optimization.

## Project Layout

```
FC-allocation/
├── requirements.txt
├── setup.py
├── src/
│   └── fc_allocation_algorithm/
│       ├── __init__.py
│       ├── analysis.py
│       ├── cli.py
│       ├── config.py
│       ├── data_processing.py
│       ├── optimiser.py
│       └── utils.py
├── test/
│   ├── already-taken.csv
│   ├── LS-detail.csv
│   └── preferences.csv
├── data/
│   ├── already-taken.csv
│   ├── LS-detail.csv
│   └── preferences.csv
└── output/
    └── course_assignments.csv
```

- **setup.py**: Package configuration and installation script.
- **requirements.txt**: List of Python dependencies.
- **src/fc_allocation_algorithm/**: Main source code for the allocation algorithm.
- **test/**: Example/test data files.
- **output/**: Directory for generated assignment results.

## Installation

1. **Clone the repository** (if you haven't already):

    ```bash
    git clone <repo-url>
    cd FC-allocation
    ```

2. **Install the package and dependencies**:

    ```bash
    pip install .
    ```

    This will automatically install all dependencies listed in `requirements.txt`.

## Usage

After installation, you can run the allocation algorithm from the command line:

```bash
fc-optimize --mode data -o output/course_assignments.csv
```

- `--mode data`: Uses real data files (default).
- `--mode test`: Uses test data from the `test/` directory.
- `-o <output_file>`: Specify the output CSV file for assignments.

### Example (using test data):

```bash
fc-optimize --mode test -o output/test_assignments.csv
```

## Input Data

- **Course Data**: Contains timings, capacities, and section info.
- **Student Preferences**: Student-course-section preferences and rankings.
- **Already Taken**: Courses/sections already assigned to students.

Default file locations are handled by the code, but you can override them in test mode.

## Output

The output CSV will contain the assigned courses and sections for each student. Summary statistics are printed to the console.

## Extending

- Add new constraints or modify optimization logic in `optimiser.py`.
- Update data processing logic in `data_processing.py`.
- Add new analysis or reporting in `analysis.py`.

## Troubleshooting

- Ensure `requirements.txt` is present in the root directory.
- Run in a clean Python environment for best results.
- For development, use editable install:  
  ```bash
  pip install -e .
  ```