#!/bin/bash

set -e

SCRIPT_FILE_PATH="$(realpath "${BASH_SOURCE[0]}")"
SCRIPT_FILE_DIRECTORY_PATH="$(dirname "${SCRIPT_FILE_PATH}")"
BASE_PROJECT_PATH="$(dirname "${SCRIPT_FILE_DIRECTORY_PATH}")"

MYPY_FILE_CONFIG="${BASE_PROJECT_PATH}/setup.cfg"
BASE_SOURCE_CODE="${BASE_PROJECT_PATH}/src"

echo "Checking pending migrations..."
./manage.py makemigrations --check

cd $BASE_SOURCE_CODE

echo "Running flake8..."
flake8 .

echo "Running mypy..."
mypy --config-file="${MYPY_FILE_CONFIG}" .
