"""Ready-mix concrete selection and source-specific ILCD normalization."""
import copy
import re
import xml.etree.ElementTree as ET

TARGET_CLASSIFICATION = "Mineral building products > Mortar and Concrete > Ready mixed concrete"


OEKO_CATEGORY_VALUE = "Beton"


def build_category_dict(xml_element):
    category_id = xml_element.get("id")
    category_name = xml_element.get("name")
    children_dict = {}

    for child_elem in xml_element.findall("{*}category"):
        child_data = build_category_dict(child_elem)
        children_dict[child_data["name"]] = child_data

    return {
        "id": category_id,
        "name": category_name,
        "children": children_dict,
    }


def parse_category_xml(xml_path):
    tree = ET.parse(xml_path, parser=ET.XMLParser(encoding="utf-8"))
    root = tree.getroot()
    category_system = root.find('.//{*}categories[@dataType="Process"]')
    top_level_dict = {}

    if category_system is not None:
        for cat_elem in category_system.findall("{*}category"):
            cat_data = build_category_dict(cat_elem)
            top_level_dict[cat_data["name"]] = cat_data

    return top_level_dict


def get_category_path_info(category_hierarchy, categories_dict):
    path_info = []
    current_dict = categories_dict

    for index, cat_name in enumerate(category_hierarchy):
        if cat_name not in current_dict:
            raise ValueError(f"Category '{cat_name}' not found at level {index}.")
        this_cat = current_dict[cat_name]
        path_info.append((this_cat["name"], this_cat["id"]))
        current_dict = this_cat["children"]

    return path_info


def first_classification_name(doc_data):
    classifications = (
        doc_data.get("processInformation", {})
        .get("dataSetInformation", {})
        .get("classificationInformation", {})
        .get("classification", [])
    )
    return classifications[0].get("name") if classifications else "Unknown"


def base_name_value(doc_data):
    base_names = (
        doc_data.get("processInformation", {})
        .get("dataSetInformation", {})
        .get("name", {})
        .get("baseName", [])
    )
    return base_names[0].get("value", "") if base_names else ""


def remove_a1_a2_a3_entries(doc_data):
    exchanges = doc_data.get("exchanges", {}).get("exchange", [])
    for exchange in exchanges:
        other = exchange.get("other", {})
        anies = other.get("anies", [])
        other["anies"] = [item for item in anies if item.get("module") not in ["A1", "A2", "A3"]]

    lcia_results = doc_data.get("LCIAResults", {}).get("LCIAResult", [])
    for lcia in lcia_results:
        other = lcia.get("other", {})
        anies = other.get("anies", [])
        other["anies"] = [item for item in anies if item.get("module") not in ["A1", "A2", "A3"]]


def sum_a1_a2_a3(doc_data):
    def handle_anies(anies_list):
        if not anies_list:
            return anies_list

        sum_value = 0.0
        sum_item_template = None
        keepers = []

        for item in anies_list:
            module = item.get("module")
            if module in ["A1", "A2", "A3"]:
                try:
                    sum_value += float(item.get("value"))
                except (TypeError, ValueError):
                    pass
                if sum_item_template is None:
                    sum_item_template = dict(item)
            else:
                keepers.append(item)

        if sum_item_template is not None:
            sum_item_template["module"] = "A1-A3"
            sum_item_template["value"] = str(sum_value)
            keepers.insert(0, sum_item_template)

        return keepers

    exchanges = doc_data.get("exchanges", {}).get("exchange", [])
    for exchange in exchanges:
        other = exchange.get("other", {})
        other["anies"] = handle_anies(other.get("anies", []))

    lcia_results = doc_data.get("LCIAResults", {}).get("LCIAResult", [])
    for lcia in lcia_results:
        other = lcia.get("other", {})
        other["anies"] = handle_anies(other.get("anies", []))


def inject_oekobau_classification(doc_data, categories_dict):
    category_names = [item.strip() for item in TARGET_CLASSIFICATION.split(">")]
    path_info = get_category_path_info(category_names, categories_dict)
    class_array = []

    for level, (cat_name, cat_id) in enumerate(path_info):
        class_array.append(
            {
                "value": cat_name,
                "level": level,
                "classId": cat_id,
            }
        )

    new_classification_item = {
        "class": class_array,
        "name": "OEKOBAU.DAT",
    }

    process_info = doc_data.setdefault("processInformation", {})
    data_set_info = process_info.setdefault("dataSetInformation", {})
    classification_info = data_set_info.setdefault("classificationInformation", {})
    existing_classifications = classification_info.get("classification")

    if not isinstance(existing_classifications, list):
        existing_classifications = []

    existing_classifications.append(new_classification_item)
    classification_info["classification"] = existing_classifications


def unify_material_property(material_property):
    name_lower = material_property.get("name", "").lower()
    material_property["name"] = re.sub(r"\(.*?\)", "", material_property.get("name", "")).strip()

    if "compressive" in name_lower:
        material_property["name"] = "compressive strength"
        material_property["unit"] = "MPa"
        material_property["unitDescription"] = "megapascals"
    elif "density" in name_lower:
        material_property["name"] = "gross density"
        material_property["unit"] = "kg/m^3"
        material_property["unitDescription"] = "kilograms per cubic meter"


def ties_has_required_properties(doc_data):
    compressive_found = False
    density_found = False

    exchanges = doc_data.get("exchanges", {}).get("exchange", [])
    for exchange in exchanges:
        for material_property in exchange.get("materialProperties", []):
            name_lower = material_property.get("name", "").lower()
            if "compressive" in name_lower and "density" not in name_lower:
                compressive_found = True
            if "density" in name_lower and "compressive" not in name_lower:
                density_found = True
            if compressive_found and density_found:
                return True

    return False


def prepare_oeko_record(uuid_value, classification_system, doc_data, next_id):
    doc_copy = copy.deepcopy(doc_data)
    product_name = base_name_value(doc_copy)
    match = re.search(r"C\s*(\d+)\s*/\s*(\d+)", product_name, flags=re.IGNORECASE)
    if not match:
        return None

    exchanges = doc_copy.get("exchanges", {}).get("exchange", [])
    if not exchanges:
        return None

    exchanges[0].setdefault("materialProperties", []).append(
        {
            "name": "compressive strength",
            "value": match.group(2),
            "unit": "MPa",
            "unitDescription": "megapascals",
        }
    )

    return {
        "id": next_id,
        "uuid": uuid_value,
        "epd_name": product_name,
        "classificationSys": classification_system,
        "document": doc_copy,
    }


def insert_compressive_strength_from_name(doc_data):
    product_name = base_name_value(doc_data)
    if not product_name:
        return

    match = re.search(r"B\s?(\d{2})|C(\d{2})/(\d{2})", product_name, re.IGNORECASE)
    if not match:
        return

    compressive_value = match.group(1) if match.group(1) else match.group(3)
    exchanges = doc_data.get("exchanges", {}).get("exchange", [])
    if not exchanges:
        return

    exchanges[0].setdefault("materialProperties", []).append(
        {
            "name": "compressive strength",
            "value": compressive_value,
            "unit": "MPa",
            "unitDescription": "megapascals",
        }
    )


def insert_gross_density_from_volume_mass(doc_data):
    exchanges = doc_data.get("exchanges", {}).get("exchange", [])
    if not exchanges:
        return

    flow_properties = exchanges[0].get("flowProperties", [])
    found_volume = False
    found_mass = False
    mass_value = None

    for flow_property in flow_properties:
        names = flow_property.get("name", [])
        mean_value = flow_property.get("meanValue")
        reference_unit = flow_property.get("referenceUnit", "")

        if any("volum" in item.get("value", "").lower() or "volume" in item.get("value", "").lower() for item in names):
            if mean_value == 1 and reference_unit == "m3":
                found_volume = True

        if any("mass" in item.get("value", "").lower() or "masse" in item.get("value", "").lower() for item in names):
            try:
                mass_value = float(mean_value)
                found_mass = True
            except (TypeError, ValueError):
                pass

    if found_volume and found_mass and mass_value is not None:
        exchanges[0].setdefault("materialProperties", []).append(
            {
                "name": "gross density",
                "value": str(mass_value),
                "unit": "kg/m^3",
                "unitDescription": "kilograms per cubic meter",
            }
        )


def has_material_property(doc_data, prop_name):
    exchanges = doc_data.get("exchanges", {}).get("exchange", [])
    if not exchanges:
        return False

    for material_property in exchanges[0].get("materialProperties", []):
        if material_property.get("name", "").lower() == prop_name.lower():
            return True
    return False


def get_location(doc_data):
    return (
        doc_data.get("processInformation", {})
        .get("geography", {})
        .get("locationOfOperationSupplyOrProduction", {})
        .get("location")
    )


def normalize_record(record, categories, material_decisions):
    """Select and normalize one record using repository-specific rules.

    Return (record, reason); a rejected record is None.
    """
    result = copy.deepcopy(record)
    doc = result["document"]
    source = result["repository"]
    decision = material_decisions.get(result["uuid"])
    if source in {"ies", "epdnorge"}:
        if decision is None:
            return None, "missing material decision"
        if decision != TARGET_CLASSIFICATION:
            return None, "material category is not ready-mix concrete"
        result["material_category"] = decision

    if source in {"oekobaudat", "ibu"}:
        expected_scheme = "OEKOBAU.DAT" if source == "oekobaudat" else "IBUCategories"
        scheme = result.get("source_classification_system", result.get("classificationSys", ""))
        if str(scheme).lower() != expected_scheme.lower():
            return None, "classification system differs from source selector"
        classifications = doc.get("processInformation", {}).get("dataSetInformation", {}).get("classificationInformation", {}).get("classification", [])
        if not any(item.get("value") == OEKO_CATEGORY_VALUE for group in classifications for item in group.get("class", [])):
            return None, "no Beton classification"
        if not any("compressive" in prop.get("name", "").lower() or "density" in prop.get("name", "").lower() for exchange in doc.get("exchanges", {}).get("exchange", []) for prop in exchange.get("materialProperties", [])):
            return None, "no strength or density property"
        prepared = prepare_oeko_record(result["uuid"], expected_scheme, doc, result["id"])
        if prepared is None:
            return None, "missing Cxx/yy name or exchange"
        result.update(prepared)
    elif source == "ies":
        if not ties_has_required_properties(doc):
            return None, "missing strength or density property"
        inject_oekobau_classification(doc, categories)
        for exchange in doc.get("exchanges", {}).get("exchange", []):
            for prop in exchange.get("materialProperties", []):
                if "compressive" in prop.get("name", "").lower() or "density" in prop.get("name", "").lower():
                    unify_material_property(prop)
        remove_a1_a2_a3_entries(doc)
    elif source == "epdnorge":
        if not get_location(doc):
            return None, "missing geographic location"
        insert_compressive_strength_from_name(doc)
        insert_gross_density_from_volume_mass(doc)
        if not has_material_property(doc, "compressive strength") or not has_material_property(doc, "gross density"):
            return None, "missing first-exchange strength or density"
        sum_a1_a2_a3(doc)
        inject_oekobau_classification(doc, categories)
    else:
        raise ValueError(f"Unsupported repository: {source}")
    return result, "accepted"
