# OptIMIIst

A Python package for advanced process discovery using the OptIMIIst algorithm. OptIMIIst is a process discovery technique that guarantees soundness while effectively handling both infrequent and incomplete behavior in event logs.

## About OptIMIIst

OptIMIIst is built on the Inductive Miner framework and operates in two steps:
1. It recursively constructs tree-structured process models
2. It uses Integer Linear Programming (ILP) to locally optimize mining decisions

Key advantages of OptIMIIst:
- Guarantees sound process models
- Handles infrequent and incomplete behavior in event logs
- Discovers locally optimal process trees
- Provides high-quality models with competitive fitness, precision, and simplicity

This package enables you to apply the OptIMIIst algorithm to your event logs and generate Petri nets, process trees, or BPMN models.

## Installation

The package is not yet available on PyPI. You can install it directly from the GitHub repository:

```bash
pip install git+https://github.com/Lalaluka/OptIMIIst.git
```

Or clone the repository and install in development mode:

```bash
git clone https://github.com/Lalaluka/OptIMIIst.git
cd OptIMIIst
pip install -e .
```

## Usage

### Command Line Interface

The package provides a command-line interface for processing event logs:

```bash
# Process an XES file and save the resulting Petri net as PNML
optimiist process input_log.xes output_model.pnml

# Process a compressed XES.GZ file
optimiist process input_log.xes.gz output_model.pnml

# Disable filtering
optimiist process input_log.xes output_model.pnml --no-filter
```

### Python API

You can also use the package as a library in your Python code:

```python
import pm4py
from optimiist import optimiist

# Load an event log
log = pm4py.read_xes('input_log.xes')

# Apply the OptIMIIst algorithm to discover a Petri net
petri_net, initial_marking, final_marking = optimiist(log, filter=True)

# Save the Petri net as PNML
pm4py.write_pnml(petri_net, initial_marking, final_marking, 'output_model.pnml')
```

## Advanced Usage

The package also exposes other functions for more advanced usage:

```python
from optimiist import optimiist_tree, optimiist_bpmn

# Get a process tree instead of a Petri net
process_tree = optimiist_tree(log, filter=True)

# Get a BPMN model
bpmn_model = optimiist_bpmn(log, filter=True)
```

## Performance Optimization

### Using Alternative LP Solvers

The OptIMIIst algorithm uses PuLP for solving linear programming problems during the filtering process. You can configure which solver to use through the 'SOLVER' environment variable:

```bash
# Set the solver to use (must be a valid PuLP solver name)
export SOLVER="PULP_CBC_CMD"
```

By default, the system uses PuLP's built-in CBC solver (PULP_CBC_CMD) if the 'SOLVER' environment variable is not set.

You can also configure solver-specific paths and parameters through their respective environment variables:

```bash
# Example: Configure the path to the CBC executable
export PULP_CBC_CMD="/path/to/cbc/executable"
```

PuLP supports various open-source and commercial solvers. Using alternative solvers can significantly improve performance for large event logs, especially when filtering is enabled. Please refer to the PuLP documentation for information about available solvers and their configuration.

## Development

### Running Tests

To run the unit tests for this package, use the following command:

```bash
python3 -m unittest discover -p '*_test.py'
```

This will discover and run all test files that end with `_test.py` in the project.

### Evaluation Scripts

The `evaluation` folder contains scripts for evaluating the OptIMIIst algorithm on both the Process Discovery Contest data from 2024 and real-life event logs. These scripts are not part of the Python package and require additional dependencies to run.

To use the evaluation scripts:

1. Create a separate virtual environment for evaluation
2. Install the OptIMIIst package in development mode
3. Install additional dependencies as needed
4. Run the scripts in the `evaluation/RealLifeLogs` directory

Note that the evaluation scripts download event logs from public repositories and may require more disk space and processing time.

## Paper

The OptIMIIst algorithm was originally presented in the paper "Locally Optimized Process Tree Discovery" at the EdbA (Event Data & Behavioral Analytics) workshop during the 6th International Conference on Process Mining (ICPM 2024).

A journal extension of this work with comprehensive details about the algorithm, its theoretical foundations, and experimental evaluation is currently awaiting publication.

**Note:** The implementation in this package is the extended version developed for the journal publication, which includes significant improvements over the algorithm presented in the original workshop paper.
