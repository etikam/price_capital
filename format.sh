#!/bin/bash

# Activate virtual environment if needed
# source env/bin/activate  # Uncomment if using a virtual environment

# Sort imports
isort .

# Format code with Black
black .

# Run Flake8 to check style
flake8 .
