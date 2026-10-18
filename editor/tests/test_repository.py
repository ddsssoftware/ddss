"""Tests for reading and writing the owned collection files."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pytest

from editor.models import records
from editor.models.records import (
    Citation,
    Condition,
    RecordError,
    Symptom,
    Test,
)
from editor.models.repository import (
    UNOWNED_COLLECTION_FILES,
    CollectionRepository,
)


def _repository(data_directory: Path) -> CollectionRepository:
    return CollectionRepository(data_directory)


def _write(data_directory: Path, filename: str, payload: object) -> Path:
    path = data_directory / filename
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _copy_of_the_shipped_data(tmp_path: Path) -> Path:
    data = tmp_path / "data"
    shutil.copytree(records.DEFAULT_DATA_DIRECTORY, data)
    return data


# -- reading ----------------------------------------------------------------


def test_load_returns_the_stored_records(tmp_path: Path) -> None:
    _write(tmp_path, "conditions.json", [{"id": "a"}, {"id": "b"}])

    loaded = _repository(tmp_path).load("conditions")

    assert [record.to_dict() for record in loaded] == [{"id": "a"}, {"id": "b"}]
    assert all(isinstance(record, Condition) for record in loaded)


def test_each_entity_type_loads_its_own_class(tmp_path: Path) -> None:
    repository = _repository(tmp_path)
    for entity_type in records.ENTITY_TYPES:
        repository.save(entity_type, [])

    loaded = {
        entity_type: repository.load(entity_type)
        for entity_type in records.ENTITY_TYPES
    }

    assert set(loaded) == set(records.ENTITY_TYPES)
    assert isinstance(repository.load("symptoms"), list)
    assert repository.record_type("citations") is Citation
    assert repository.path("tests") == tmp_path / "tests.json"


def test_load_all_reads_every_owned_collection(tmp_path: Path) -> None:
    repository = _repository(tmp_path)
    for entity_type in records.ENTITY_TYPES:
        repository.save(entity_type, [])

    assert set(repository.load_all()) == set(records.ENTITY_TYPES)


def test_load_rejects_a_non_array_file(tmp_path: Path) -> None:
    _write(tmp_path, "conditions.json", {"id": "not-an-array"})

    with pytest.raises(RecordError, match="must contain a JSON array"):
        _repository(tmp_path).load("conditions")


def test_load_rejects_malformed_json(tmp_path: Path) -> None:
    (tmp_path / "conditions.json").write_text("not json at all", encoding="utf-8")

    with pytest.raises(RecordError, match="not valid JSON"):
        _repository(tmp_path).load("conditions")


def test_load_rejects_non_object_items(tmp_path: Path) -> None:
    _write(tmp_path, "conditions.json", ["a string"])

    with pytest.raises(RecordError, match="must be a JSON object"):
        _repository(tmp_path).load("conditions")


def test_load_reports_a_missing_file(tmp_path: Path) -> None:
    with pytest.raises(RecordError, match="Could not read"):
        _repository(tmp_path).load("conditions")


def test_an_unknown_entity_type_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(RecordError, match="Unknown entity type"):
        _repository(tmp_path).load("cases")


def test_the_shipped_data_directory_loads() -> None:
    assert isinstance(_repository(None).load("conditions"), list)


# -- writing ----------------------------------------------------------------


def test_save_writes_a_json_array_of_the_data_model_fields(tmp_path: Path) -> None:
    path = _repository(tmp_path).save(
        "conditions", [Condition(id="a", name="A", symptoms=["s1"], aka=[])]
    )

    payload = json.loads(path.read_text(encoding="utf-8"))

    assert isinstance(payload, list)
    assert payload == [{"id": "a", "name": "A", "symptoms": ["s1"], "aka": []}]


def test_save_omits_unset_fields(tmp_path: Path) -> None:
    path = _repository(tmp_path).save("citations", [Citation(id="a")])

    assert json.loads(path.read_text(encoding="utf-8")) == [{"id": "a"}]


def test_unrelated_records_survive_a_write(tmp_path: Path) -> None:
    repository = _repository(tmp_path)
    repository.save(
        "conditions",
        [Condition(id="a", name="First"), Condition(id="b", name="Second")],
    )

    loaded = repository.load("conditions")
    loaded[0].name = "Changed"
    repository.save("conditions", loaded)

    reloaded = repository.load("conditions")
    assert reloaded[0].name == "Changed"
    assert reloaded[1] == Condition(id="b", name="Second")


def test_save_leaves_no_temporary_file_behind(tmp_path: Path) -> None:
    _repository(tmp_path).save("tests", [Test(id="a")])

    assert [p.name for p in tmp_path.iterdir() if p.name.endswith(".tmp")] == []


def test_save_creates_a_missing_directory(tmp_path: Path) -> None:
    repository = _repository(tmp_path / "missing" / "data")

    repository.save("tests", [Test(id="a")])

    assert repository.load("tests") == [Test(id="a")]


def test_save_reports_a_write_failure(tmp_path: Path) -> None:
    blocker = tmp_path / "not-a-directory"
    blocker.write_text("not a directory", encoding="utf-8")

    with pytest.raises(RecordError):
        _repository(blocker).save("tests", [Test(id="a")])


def test_a_failed_write_leaves_the_previous_file_intact(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repository = _repository(tmp_path)
    repository.save("tests", [Test(id="a", name="Before")])

    def explode(self: Path, target: Path) -> None:
        raise OSError("disk full")

    monkeypatch.setattr(Path, "replace", explode)

    with pytest.raises(RecordError, match="Could not write"):
        repository.save("tests", [Test(id="b", name="After")])

    assert repository.load("tests") == [Test(id="a", name="Before")]


# -- key order is not part of the contract ----------------------------------


def test_a_stored_object_loads_the_same_whatever_the_key_order(
    tmp_path: Path,
) -> None:
    _write(
        tmp_path,
        "conditions.json",
        [{"aka": [], "priority": 1, "name": "A", "id": "a"}],
    )

    assert _repository(tmp_path).load("conditions") == [
        Condition(id="a", name="A", priority=1, aka=[])
    ]


def test_a_real_record_with_shuffled_keys_loads_unchanged(tmp_path: Path) -> None:
    data = _copy_of_the_shipped_data(tmp_path)
    repository = _repository(data)
    original = repository.load("conditions")[0]

    shuffled = dict(reversed(list(original.to_dict().items())))
    _write(data, "conditions.json", [shuffled])

    assert repository.load("conditions") == [original]


def test_a_copy_of_the_shipped_data_round_trips(tmp_path: Path) -> None:
    repository = _repository(_copy_of_the_shipped_data(tmp_path))

    loaded = repository.load_all()
    for entity_type, collection in loaded.items():
        repository.save(entity_type, collection)

    assert repository.load_all() == loaded


# -- the collections the editor does not own --------------------------------


def test_the_owned_files_are_never_a_client_only_collection() -> None:
    owned = {record_class.FILENAME for record_class in records.RECORD_TYPES.values()}

    assert owned.isdisjoint(UNOWNED_COLLECTION_FILES)
    assert len(owned) == len(records.ENTITY_TYPES)


def test_the_client_only_collections_are_neither_read_nor_written(
    tmp_path: Path,
) -> None:
    repository = _repository(tmp_path)
    for filename in UNOWNED_COLLECTION_FILES:
        _write(tmp_path, filename, [{"id": "untouched"}])
    for entity_type in records.ENTITY_TYPES:
        repository.save(entity_type, [])

    assert set(repository.load_all()) == set(records.ENTITY_TYPES)
    for filename in UNOWNED_COLLECTION_FILES:
        assert json.loads((tmp_path / filename).read_text(encoding="utf-8")) == [
            {"id": "untouched"}
        ]


# -- the published data version ---------------------------------------------


def test_a_save_publishes_the_write_time_as_the_version(tmp_path: Path) -> None:
    moment = datetime(2026, 10, 18, 14, 3, 11, 482123, tzinfo=timezone.utc)
    repository = CollectionRepository(tmp_path, clock=lambda: moment)

    repository.save("tests", [Test(id="a")])

    assert json.loads((tmp_path / "version.json").read_text(encoding="utf-8")) == {
        "version": "2026-10-18T14:03:11.482123Z"
    }


def test_a_naive_clock_value_is_treated_as_utc(tmp_path: Path) -> None:
    naive = datetime(2026, 10, 18, 14, 3, 11, 482123)
    repository = CollectionRepository(tmp_path, clock=lambda: naive)

    repository.save("tests", [])

    assert json.loads((tmp_path / "version.json").read_text(encoding="utf-8")) == {
        "version": "2026-10-18T14:03:11.482123Z"
    }


def test_the_version_is_written_after_the_collection(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    replaced: list[str] = []
    original = Path.replace

    def record(self: Path, target: Path) -> Path:
        replaced.append(Path(target).name)
        return original(self, target)

    monkeypatch.setattr(Path, "replace", record)

    _repository(tmp_path).save("tests", [Test(id="a")])

    assert replaced == ["tests.json", "version.json"]


def test_a_failed_version_write_does_not_fail_the_save(tmp_path: Path) -> None:
    repository = _repository(tmp_path)
    (tmp_path / "version.json").mkdir()

    repository.save("tests", [Test(id="a")])

    assert repository.load("tests") == [Test(id="a")]

    (tmp_path / "version.json").rmdir()
    repository.save("tests", [Test(id="b")])

    assert (tmp_path / "version.json").is_file()
