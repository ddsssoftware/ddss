#!/bin/bash
#
# Run the SSEditor unit tests with coverage reporting.
#
# Line and branch coverage is measured for the `editor` package (see the
# [tool.coverage.*] sections in pyproject.toml) and printed to the terminal,
# with a browsable HTML report written to coverage/html.
#
# Any arguments are forwarded to pytest, e.g.:
#   ./run_unit_test.sh -k rules
#   ./run_unit_test.sh --cov-report=xml
set -euo pipefail

cd "$(dirname "$0")/.." || exit 1
.venv/bin/python -m pytest -q --cov-report=html