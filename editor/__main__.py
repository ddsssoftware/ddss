"""Entry point for ``python -m editor`` and the ``sseditor`` console script."""

from __future__ import annotations

from editor.app import EditorApp


def main() -> None:
    """Run the SSEditor terminal application."""
    EditorApp().run()


if __name__ == "__main__":
    main()
