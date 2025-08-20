from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name='fc_allocation_algorithm',
    version='0.1',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=parse_requirements("requirements.txt"),
    entry_points={
        'console_scripts': [
            'fc-optimize=fc_allocation_algorithm.cli:main',
        ],
    },
)