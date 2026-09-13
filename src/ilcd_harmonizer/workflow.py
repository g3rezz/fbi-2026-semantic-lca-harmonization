"""Source normalization, semantic enrichment, and harmonized graph construction."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

import yaml
from rdflib import Literal, RDF, URIRef
from rdflib.namespace import DCTERMS

from .decisions import load_din_decisions, load_material_decisions
from .inputs import load_records, read_jsonl, write_json, write_jsonl
from .normalization import normalize_record, parse_category_xml

RESOURCES = Path(__file__).parent / "resources"


def load_config(path: Path):
    path = path.resolve()
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(config, dict) or "input" not in config or "output_dir" not in config:
        raise ValueError("Configuration requires input and output_dir")

    def resolve(value):
        candidate = Path(value).expanduser()
        return candidate.resolve() if candidate.is_absolute() else (path.parent / candidate).resolve()

    return config, resolve


def diagnose(config, resolve):
    records = load_records(config, resolve)
    properties, modules = Counter(), Counter()
    for record in records:
        for exchange in record["document"].get("exchanges", {}).get("exchange", []):
            properties.update(prop.get("name", "") for prop in exchange.get("materialProperties", []))
        for result in record["document"].get("LCIAResults", {}).get("LCIAResult", []):
            modules.update(item["module"] for item in result.get("other", {}).get("anies", []) if isinstance(item, dict) and "module" in item)
    report = {"records": len(records), "repositories": dict(Counter(row["repository"] for row in records)), "material_property_occurrences": dict(properties), "lcia_module_occurrences": dict(modules)}
    write_json(resolve(config["output_dir"]) / "diagnostics.json", report)
    return report


def normalize(config, resolve):
    records = load_records(config, resolve)
    selected, report = [], []
    decisions = load_material_decisions(config.get("material_decisions"), resolve, config.get("material_rules"))
    if config["input"].get("mode", "raw") == "normalized":
        selected = records
        report = [{"uuid": row["uuid"], "repository": row["repository"], "reason": "normalized input"} for row in records]
    else:
        resources = config["resources"]
        categories = parse_category_xml(resolve(resources.get("category_api", resources["category_en"])))
        for record in records:
            result, reason = normalize_record(record, categories, decisions)
            report.append({"uuid": record["uuid"], "repository": record["repository"], "reason": reason})
            if result is not None:
                selected.append(result)
    if config.get("selection_uuids"):
        requested = config["selection_uuids"]
        lookup = {row["uuid"]: row for row in selected}
        if len(set(requested)) != len(requested) or set(requested) - lookup.keys():
            raise ValueError("selection_uuids contains duplicates or unaccepted UUIDs")
        selected = [lookup[uuid] for uuid in requested]
    output = resolve(config["output_dir"])
    selected_ids = {row["uuid"] for row in selected}
    for entry in report:
        entry["selected"] = entry["uuid"] in selected_ids
    write_json(output / "normalization-report.json", {"input_records": len(records), "accepted_records": len(selected), "records": report})
    if not selected:
        raise ValueError("No accepted records; see normalization-report.json")
    for index, row in enumerate(selected, 1):
        row["id"] = index
    write_jsonl(output / "normalized.jsonl", selected)
    return {"normalized_records": len(selected)}


def enrich(config, resolve):
    output = resolve(config["output_dir"])
    records = read_jsonl(output / "normalized.jsonl")
    decisions = load_din_decisions(config.get("din_decisions"), resolve)
    missing = [row["uuid"] for row in records if row["uuid"] not in decisions]
    if missing:
        raise ValueError(f"Missing DIN decisions for {len(missing)} records: {missing[:3]}")
    for row in records:
        row["cost_group_codes"] = decisions[row["uuid"]]
    write_jsonl(output / "enriched.jsonl", records)
    return {"enriched_records": len(records)}


def add_sources(graph, records):
    from .graph import find_top_epd_node_by_uuid

    graph.bind("dcterms", DCTERMS)
    for row in records:
        epd = find_top_epd_node_by_uuid(graph, row["uuid"])
        if epd is None:
            raise ValueError(f"Cannot attach source: no EPD node for {row['uuid']}")
        source = URIRef(row["repository_uri"])
        graph.add((epd, DCTERMS.source, source))
        graph.add((source, DCTERMS.title, Literal(row["repository"])))


def build(config, resolve):
    from .graph import (ILCD, CC, build_modified_json_docs, generate_graph_from_docs,
                        unify_ns_prefixes_graph, enrich_canonical_skos, enrich_din, enrich_bki)
    from .inference import classify_properties

    output = resolve(config["output_dir"])
    records = read_jsonl(output / "enriched.jsonl")
    if not records:
        raise ValueError("No enriched records")
    docs = build_modified_json_docs(records, RESOURCES / "schemas/linkml_ILCDmergedSchemas_schema.yaml")
    graph, failures = generate_graph_from_docs(docs, RESOURCES / "schemas/linkml_processDataSet_schema.yaml", validate_docs=True)
    if failures:
        raise ValueError(f"LinkML loading failed for {len(failures)} records")
    graph = unify_ns_prefixes_graph(graph)
    resources = config["resources"]
    enrich_canonical_skos(graph, resolve(resources["category_en"]), resolve(resources["category_de"]))
    enrich_din(graph, {row["uuid"]: row["cost_group_codes"] for row in records}, resolve(resources["din_csv"]))
    enrich_bki(graph, [resolve(path) for path in resources.get("bki_xml", [])])
    print("Executing SHACL strength and density rules", flush=True)
    conforms, report, _ = classify_properties(graph, RESOURCES / "shacl/concrete_class_shacl_shapes.ttl")
    add_sources(graph, records)
    graph.serialize(output / "graph.ttl", format="turtle")
    report.serialize(output / "shacl-report.ttl", format="turtle")
    normalization_report = json.loads((output / "normalization-report.json").read_text(encoding="utf-8"))
    summary = {
        "input_records": normalization_report["input_records"],
        "accepted_records": len(records),
        "graph_records": len(set(graph.subjects(RDF.type, ILCD.ProcessDataSet))),
        "repositories": dict(Counter(row["repository"] for row in records)),
        "strength_classified_records": len(set(graph.subjects(CC.hasStrengthClassification))),
        "density_classified_records": len(set(graph.subjects(CC.hasWeightClassification))),
        "graph_path": "graph.ttl",
        "shacl_conforms": conforms,
    }
    write_json(output / "run-summary.json", summary)
    return summary


def execute(command: str, config_path: Path):
    config, resolve = load_config(config_path)
    if command == "prepare":
        from .preparation import prepare
        return prepare(config, resolve)
    commands = {"diagnose": diagnose, "normalize": normalize, "enrich": enrich, "build": build}
    if command == "run":
        normalize(config, resolve)
        enrich(config, resolve)
        return build(config, resolve)
    return commands[command](config, resolve)
