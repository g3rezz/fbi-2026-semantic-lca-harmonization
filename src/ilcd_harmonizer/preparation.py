"""Prepare local IES fields for the deterministic material rules."""
import csv
import re

from .inputs import load_records

ALLOWED_CATEGORIES = {
    "construction products, infrastructure and buildings",
    "construction products",
    "",
}

# Order and substring replacement are part of the text preparation procedure.
SYNONYMS = {
    "kilogram": "kg", "kilograms": "kg", "gram": "g", "grams": "g",
    "liter": "L", "liters": "L", "metre": "m", "meter": "m",
    "centimetre": "cm", "centimeter": "cm", "millimetre": "mm", "millimeter": "mm",
}
FIELDS = (
    "UUID", "Product Name", "Technology Description", "Technological Applicability",
    "Flow Property Name", "Flow Property Mean Value", "Flow Property Reference Unit",
)


def clean_text(text, lowercase=True):
    if not isinstance(text, str):
        return "N/A"
    text = re.sub(r"\s+", " ", text.strip().replace("\n", " "))
    if lowercase:
        text = text.lower()
    text = text.replace("&", "and")
    text = re.sub(r"[^a-zA-Z0-9.:,\-_/()\s]", "", text)
    for key, value in SYNONYMS.items():
        text = text.replace(key, value)
    return text


def extract_material_fields(document):
    """Select the study's text and flow fields; retain first-entry selection."""
    process = document.get("processInformation", {})
    info = process.get("dataSetInformation", {})
    technology = process.get("technology", {})
    name = clean_text(info.get("name", {}).get("baseName", [{}])[0].get("value", ""), lowercase=False)
    classifications = info.get("classificationInformation", {}).get("classification", [])
    classification = clean_text(classifications[0]["class"][0].get("value", "")) if classifications else ""
    if classification not in ALLOWED_CATEGORIES:
        return None

    description = technology.get("technologyDescriptionAndIncludedProcesses", [])
    description = clean_text(description[0].get("value", ""), lowercase=False) if description else ""
    applicability = technology.get("technologicalApplicability", [])
    applicability = (clean_text(applicability[0].get("value", ""), lowercase=False)
                     if applicability and isinstance(applicability, list) else "")

    flow_name, mean_value, reference_unit = "", "", ""
    exchanges = document.get("exchanges", {}).get("exchange", [])
    if exchanges and isinstance(exchanges, list):
        properties = exchanges[0].get("flowProperties", [])
        if properties and isinstance(properties, list):
            names = properties[0].get("name", [])
            if names and isinstance(names, list):
                flow_name = clean_text(names[0].get("value", ""), lowercase=False)
            mean_value = properties[0].get("meanValue", "")
            reference_unit = properties[0].get("referenceUnit", "")
    return dict(zip(FIELDS, (info.get("UUID", ""), name, description, applicability,
                             flow_name, mean_value, reference_unit)))


def prepare(config, resolve):
    """Write eligible IES fields locally, without loading decisions or vocabularies."""
    sources = [source for source in config["input"]["sources"] if source.get("repository") == "ies"]
    if not sources:
        raise ValueError("prepare requires an IES input source")
    settings = {**config, "input": {**config["input"], "sources": sources}}
    records = load_records(settings, resolve)
    rows = []
    for record in records:
        try:
            row = extract_material_fields(record["document"])
        except (AttributeError, IndexError, KeyError, TypeError) as exc:
            raise ValueError(f"Cannot prepare IES fields for {record['uuid']}: {exc}") from exc
        if row is not None:
            rows.append(row)
    path = resolve(config["output_dir"]) / "ies-material-fields.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return {"ies_records": len(records), "prepared_records": len(rows),
            "ineligible_category_records": len(records) - len(rows), "material_rules_path": str(path)}
