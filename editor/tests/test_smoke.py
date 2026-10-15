"""Smoke test: the editor package is importable and collected by pytest."""

from __future__ import annotations


def test_editor_package_is_importable() -> None:
    import editor

    assert editor.__doc__, "editor package should carry a docstring"


def test_app_module_exposes_the_application() -> None:
    from editor.app import EditorApp

    assert EditorApp.TITLE == "Editor"


def test_the_module_entry_point_runs_the_application(monkeypatch) -> None:
    from editor import __main__ as entry

    started: list[object] = []
    monkeypatch.setattr(entry.EditorApp, "run", lambda self: started.append(self))

    entry.main()

    assert len(started) == 1
