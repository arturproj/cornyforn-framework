#!/bin/bash
set -e

# Create .venv if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo ".venv created."
else
    echo ".venv already exists."
fi

# Activate the virtual environment
source .venv/bin/activate
# Install required packages
pip install --upgrade pip
pip install -r requirements.txt

# Check Python version
python_version=$(python --version 2>&1)

echo "Virtual environment activated. Python version: $python_version"

python src/app.py
