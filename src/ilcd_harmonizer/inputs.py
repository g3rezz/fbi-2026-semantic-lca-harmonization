"""Read local ILCD records and retain their source identifiers and classifications."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

REPOSITORIES = {"oekobaudat", "ibu", "epdnorge", "ies"}


def read_jsonl(path: Path) -> list[dict]:
    records = []
    with path.open(encoding="utf-8-sig") as stream:
        for number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.name}, line {number}: invalid JSON") from exc
            if not isinstance(record, dict):
                raise ValueError(f"{path.name}, line {number}: expected an object")
            records.append(record)
    return records


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")


def prepare_record(item: dict, source: dict, metadata=None) -> dict:
    document = item.get("document", item)
    info = document["processInformation"]["dataSetInformation"]
    uuid = str(info["UUID"])
    if "document" in item and str(item.get("uuid", uuid)) != uuid:
        raise ValueError("Record UUID differs from its document UUID")
    names = info.get("name", {}).get("baseName", [])
    classifications = info.get("classificationInformation", {}).get("classification", [])
    scheme = item.get("classificationSys", classifications[0].get("name", "") if classifications else "")
    return {
        "id": item.get("id", uuid),
        "uuid": uuid,
        "epd_name": item.get("epd_name", names[0].get("value", "") if names else ""),
        "classificationSys": scheme,
        "source_classification_system": metadata["classification_system"] if metadata else item.get("source_classification_system", scheme),
        "repository": source["repository"],
        "repository_uri": source["repository_uri"],
        "document": document,
    }


def read_sqlite_records(path: Path, source: dict) -> list[dict]:
    connection = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            "SELECT d.document, m.classification_system FROM epd_documents d "
            "JOIN epd_metadata m ON d.uuid=m.uuid WHERE m.base_uri = ?",
            (source["base_uri"],),
        )
        records = []
        for row in rows:
            if not row["document"]:
                continue
            try:
                document = json.loads(row["document"])
            except json.JSONDecodeError:
                continue  # Only parseable API records enter source normalization.
            records.append(prepare_record({"document": document}, source, row))
        return records
    finally:
        connection.close()


def load_records(config: dict, resolve) -> list[dict]:
    settings = config["input"]
    if settings.get("mode", "raw") not in {"raw", "normalized"}:
        raise ValueError("input.mode must be raw or normalized")
    records = []
    for source in settings["sources"]:
        if source.get("repository") not in REPOSITORIES:
            raise ValueError(f"Unknown repository: {source.get('repository')}")
        if not str(source.get("repository_uri", "")).startswith(("https://", "http://")):
            raise ValueError("Each input source requires an absolute HTTP(S) repository_uri")
        path = resolve(source["path"])
        input_format = source.get("format", "jsonl")
        if input_format == "jsonl":
            records.extend(prepare_record(item, source) for item in read_jsonl(path))
        elif input_format == "sqlite":
            records.extend(read_sqlite_records(path, source))
        else:
            raise ValueError(f"Unsupported input format: {input_format}")
    seen = set()
    for record in records:
        if record["uuid"] in seen:
            raise ValueError(f"Duplicate input UUID: {record['uuid']}; supply one record per UUID")
        seen.add(record["uuid"])
    return records
