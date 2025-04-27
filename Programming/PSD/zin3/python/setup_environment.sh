#!/bin/bash

# Configuration
VENV_NAME="psd_env"
VENV_PATH="$(pwd)/${VENV_NAME}"
PYTHON_VERSION="3.8"  # Specify the Python version you want to use
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
    python3 -m venv "$VENV_PATH"
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Please check your Python installation."
        exit 1
    fi
    echo "Virtual environment created successfully."
else
    echo "Virtual environment already exists at $VENV_PATH."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "${VENV_PATH}/bin/activate"
if [ $? -ne 0 ]; then
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
        pip install "$package"
        if [ $? -ne 0 ]; then
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
