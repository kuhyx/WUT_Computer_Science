#!/bin/bash

# Configuration
VENV_NAME="psd_env"
VENV_PATH="$(pwd)/${VENV_NAME}"
# Recorded for reference: the interpreter this project was developed against.
# Not used by the script, which takes whatever python3 is on PATH.
export PYTHON_VERSION="3.8"
REQUIREMENTS=(
    "confluent-kafka"
    "apache-flink"
    "apache-flink-libraries"
)

echo "Setting up Python environment for PSD project..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment at $VENV_PATH..."
    if ! python3 -m venv "$VENV_PATH"; then
        echo "Failed to create virtual environment. Please check your Python installation."
        exit 1
    fi
    echo "Virtual environment created successfully."
else
    echo "Virtual environment already exists at $VENV_PATH."
fi

# Activate virtual environment
echo "Activating virtual environment..."
# shellcheck source=/dev/null
if ! source "${VENV_PATH}/bin/activate"; then
    echo "Failed to activate virtual environment."
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install required packages if not already installed
echo "Checking and installing required packages..."
for package in "${REQUIREMENTS[@]}"; do
    if ! pip show "$package" &> /dev/null; then
        echo "Installing $package..."
        if ! pip install "$package"; then
            echo "Failed to install $package."
            exit 1
        fi
    else
        echo "$package is already installed."
    fi
done

# Print success message
echo ""
echo "===================================================="
echo "Python environment setup complete!"
echo "Python version: $(python -V)"
echo "Installed packages:"
pip list
echo "===================================================="
echo ""
echo "To activate this environment in the future, run:"
echo "source ${VENV_PATH}/bin/activate"
echo ""
echo "Your environment is now active and ready to use."
echo "===================================================="
