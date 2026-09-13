"""Load UUID-keyed semantic decisions and apply deterministic material rules."""
import csv

from .inputs import read_jsonl
from .materials import classify_product


def decision_paths(paths):
    if paths is None:
        return []
    if isinstance(paths, str):
        return [paths]
    if not isinstance(paths, list) or not all(isinstance(path, str) for path in paths):
        raise ValueError("Decision inputs must be a path or list of paths")
    return paths


def add_decision(decisions, uuid, value):
    uuid = str(uuid)
    if uuid in decisions and decisions[uuid] != value:
        raise ValueError(f"Conflicting semantic decisions for {uuid}")
    decisions[uuid] = value


def load_material_decisions(paths, resolve, rule_input=None):
    decisions = {}
    for filename in decision_paths(paths):
        for row in read_jsonl(resolve(filename)):
            category = row["best_category"]
            if not isinstance(category, str):
                raise ValueError(f"Material category must be a string for {row['uuid']}")
            add_decision(decisions, row["uuid"], category)
    if rule_input:
        with resolve(rule_input).open(encoding="utf-8-sig", newline="") as stream:
            for row in csv.DictReader(stream):
                fields = [row.get(key, "") or "nan" for key in (
                    "Product Name", "Technology Description", "Technological Applicability",
                    "Flow Property Name", "Flow Property Mean Value", "Flow Property Reference Unit",
                )]
                add_decision(decisions, row["UUID"], classify_product(*fields))
    return decisions


def load_din_decisions(paths, resolve):
    decisions = {}
    for filename in decision_paths(paths):
        for row in read_jsonl(resolve(filename)):
            codes = row["cost_group_codes"]
            if not isinstance(codes, list) or any(not str(code).isdigit() or len(str(code)) != 3 for code in codes):
                raise ValueError(f"Invalid DIN codes for {row['uuid']}")
            add_decision(decisions, row["uuid"], list(dict.fromkeys(str(code) for code in codes)))
    return decisions
