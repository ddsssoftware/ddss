"""Convenience launcher for the SSEditor application.

Run this from the project root with::

    python editor.py

It starts the Textual app defined in the ``editor`` package. For the packaged
entry points use ``python -m editor`` or the ``sseditor`` console script.

If it is started with an interpreter that lacks the app dependencies (such as
the system ``python3``), the launcher transparently re-runs itself with the
project virtual environment in ``.venv``.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
VENV_DIRECTORY = PROJECT_ROOT / ".venv"
VENV_PYTHON = VENV_DIRECTORY / "bin" / "python"


def _in_project_virtualenv() -> bool:
    """Return whether the current interpreter is the project virtualenv."""
    return Path(sys.prefix) == VENV_DIRECTORY


def ensure_dependencies() -> None:
    """Re-run inside the project virtualenv when the app deps are missing."""
    try:
        import textual  # noqa: F401
    except ModuleNotFoundError:
        if not _in_project_virtualenv() and VENV_PYTHON.exists():
            # Replace this process with the virtualenv interpreter, which has
            # the dependencies installed. os.execv does not return.
            os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), *sys.argv])
        raise SystemExit(
            "SSEditor dependencies are not installed.\n"
            f"Run it with the project virtualenv: {VENV_PYTHON} editor.py\n"
            f"or install them first: {sys.executable} -m pip install -e ."
        )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse the launcher's command line arguments."""
    from editor.models.records import DEFAULT_DATA_DIRECTORY, ENTITY_TYPES

    parser = argparse.ArgumentParser(description="Start the SSEditor terminal app.")
    parser.add_argument(
        "--data-directory",
        type=Path,
        default=None,
        help=(
            "Directory holding the clinical JSON collections. "
            f"Defaults to {DEFAULT_DATA_DIRECTORY}."
        ),
    )
    parser.add_argument(
        "--entity-type",
        choices=ENTITY_TYPES,
        default=None,
        help="Open directly on this entity type instead of the home screen.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Run the SSEditor terminal application."""
    ensure_dependencies()

    from editor.app import EditorApp

    args = parse_args(argv)
    EditorApp(
        data_directory=args.data_directory,
        initial_entity_type=args.entity_type,
    ).run()


if __name__ == "__main__":
    main()
