# Test Suite

## Overview
This directory contains automated unit tests and smoke tests for the **Intelligent Traffic Management System**.

## Running Tests
Run the test suite using Python's built-in `unittest` runner (no additional packages required):

```bash
# Run tests from the repository root
python -m unittest discover -s tests
```

Or using `pytest` (if installed):
```bash
pytest tests/ -v
```

## Test Coverage
- **`tests/test_smoke.py`:**
  - Verifies configuration settings and path resolution (`src/config.py`).
  - Verifies mathematical boundaries and invariants of the adaptive signal timing algorithm (`src/traffic_analysis/signal_advisor.py`).
  - Verifies zero-traffic edge cases (no division-by-zero, legal minimum green allocation).
  - Verifies emergency preemption priority override mechanics.
  - Verifies graceful handling of missing model weights without unhandled exceptions.
