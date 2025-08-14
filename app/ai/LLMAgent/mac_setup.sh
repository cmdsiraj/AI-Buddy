#!/bin/bash

PYTHON_VERSION="3.9.6"
VENV_DIR=".venv"

echo "Checking if Python $PYTHON_VERSION is installed via pyenv..."

if ! pyenv versions --bare | grep -q "^$PYTHON_VERSION$"; then
  echo "Python $PYTHON_VERSION not found. Installing..."
  pyenv install $PYTHON_VERSION
else
  echo "Python $PYTHON_VERSION is already installed."
fi

echo "Setting local Python version to $PYTHON_VERSION..."
pyenv local $PYTHON_VERSION

# Refresh pyenv environment
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv rehash

PYTHON_PATH=$(pyenv which python)

echo "Creating virtual environment in $VENV_DIR using $PYTHON_PATH..."
$PYTHON_PATH -m venv $VENV_DIR

echo "Virtual environment created!"
echo "Activating virtual environment..."

source $VENV_DIR/bin/activate

if [ ! -f "requirements.txt" ]; then
  echo "No requirements.txt file found."
else
  echo "Installing dependencies from requirements.txt..."
  pip install -r requirements.txt
fi

echo "Done!"
