"""LinkML-to-RDF construction and shared material, planning, and BKI concepts."""
from __future__ import annotations
import copy
import csv
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
import rdflib
import yaml
from linkml.validator import Validator
from linkml_runtime.dumpers import RDFLibDumper
from linkml_runtime.loaders import YAMLLoader
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import SKOS, XSD
from ._generated.linkml_processDataSet_schema import ProcessDataSet

ILCD = Namespace("https://example.org/ilcd/")


OBD = Namespace("https://example.org/obd/")


DIN = Namespace("https://example.org/din276/")


BKI = Namespace("https://example.org/bki/")


CC = Namespace("https://example.org/concreteclass/")


LINKML_UUID = URIRef("https://w3id.org/linkml/UUIDType")


OLD_NS_LIST = (
    "ILCDex:",
    "ILCDsd:",
    "ILCDlcia:",
    "ILCDmav:",
    "ILCDadmin:",
    "ILCDpi:",
)


TARGET_CATEGORY_KEYS = {
    "mineral building products",
    "mineralische baustoffe",
    "mortar and concrete",
    "m\u00f6rtel und beton",
    "ready mixed concrete",
    "beton",
}


def format_seconds(seconds: float) -> str:
    total_seconds = max(0, int(seconds))
    minutes, secs = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:d}h {minutes:02d}m {secs:02d}s"
    if minutes:
        return f"{minutes:d}m {secs:02d}s"
    return f"{secs:d}s"


def print_loop_progress(
    label: str,
    current: int,
    total: int,
    start_time: float,
    interval: int = 10,
) -> None:
    if total <= 0:
        return
    if current != total and current % interval != 0:
        return
    elapsed = time.perf_counter() - start_time
    rate = current / elapsed if elapsed > 0 else 0.0
    remaining = total - current
    eta_seconds = remaining / rate if rate > 0 else 0.0
    print(
        f"{label}: {current}/{total} | elapsed={format_seconds(elapsed)} | "
        f"eta={format_seconds(eta_seconds)}"
    )


def recursive_rename_uri(obj: Any) -> Any:
    if isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            new_key = "refObjectUri" if key == "uri" else key
            new_obj[new_key] = recursive_rename_uri(value)
        return new_obj
    if isinstance(obj, list):
        return [recursive_rename_uri(item) for item in obj]
    return obj


def remove_raw_strings_in_anies(obj: Any) -> Any:
    if isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            if key == "anies" and isinstance(value, list):
                new_obj[key] = [
                    remove_raw_strings_in_anies(item)
                    for item in value
                    if not isinstance(item, str)
                ]
            else:
                new_obj[key] = remove_raw_strings_in_anies(value)
        return new_obj
    if isinstance(obj, list):
        return [remove_raw_strings_in_anies(item) for item in obj]
    return obj


def transform_json(data: dict[str, Any]) -> dict[str, Any]:
    process_info = data.get("processInformation", {})
    data_set_info = process_info.get("dataSetInformation", {})

    if "name" in data_set_info:
        data_set_info["dataSetName"] = data_set_info.pop("name")

    if "other" in data_set_info:
        data_set_info["otherDSI"] = data_set_info.pop("other")
        if "anies" in data_set_info["otherDSI"]:
            for item in data_set_info["otherDSI"]["anies"]:
                if isinstance(item, dict) and "componentsAndMaterialsAndSubstances" in item:
                    data_set_info["otherDSI"].pop("anies")
                    break
            if "scenario" in data_set_info["otherDSI"]:
                data_set_info["objectScenario"] = data_set_info["otherDSI"].pop("scenario")

    classification_info = data_set_info.get("classificationInformation", {})
    for cls_obj in classification_info.get("classification", []):
        if "class" in cls_obj:
            cls_obj["classEntries"] = cls_obj.pop("class")

    if "time" in process_info:
        process_info["timeInformation"] = process_info.pop("time")
        time_info = process_info["timeInformation"]
        if "other" in time_info:
            time_info["otherTime"] = time_info.pop("other")
            for item in time_info["otherTime"].get("anies", []):
                if isinstance(item, dict) and "value" in item:
                    item["timestampValue"] = item.pop("value")

    mod_val = data.get("modellingAndValidation", {})
    lci_method = mod_val.get("LCIMethodAndAllocation", {})
    if "other" in lci_method:
        lci_method["otherMAA"] = lci_method.pop("other")

    dstar = mod_val.get("dataSourcesTreatmentAndRepresentativeness", {})
    if "other" in dstar:
        dstar["otherDSTAR"] = dstar.pop("other")
        if "anies" in dstar["otherDSTAR"]:
            dstar["otherDSTAR"]["aniesDSTAR"] = dstar["otherDSTAR"].pop("anies")
            for item in dstar["otherDSTAR"]["aniesDSTAR"]:
                if isinstance(item, dict) and "value" in item and isinstance(item["value"], dict):
                    item["valueDSTAR"] = item.pop("value")
                    val = item["valueDSTAR"]
                    if "shortDescription" in val:
                        val["shortDescriptionExtended"] = val.pop("shortDescription")
                    if "version" in val:
                        version = val.pop("version")
                        if "version" in version:
                            version["versionInt"] = version.pop("version")
                        val["versionDict"] = version
                    if "uuid" in val:
                        uuid_obj = val.pop("uuid")
                        if "uuid" in uuid_obj:
                            uuid_obj["uuidValue"] = uuid_obj.pop("uuid")
                        val["uuidDict"] = uuid_obj

    if "validation" in mod_val:
        mod_val["validationInfo"] = mod_val.pop("validation")

    if "other" in mod_val:
        mod_val["otherMAV"] = mod_val.pop("other")
        for item in mod_val["otherMAV"].get("anies", []):
            if isinstance(item, dict) and "value" in item and isinstance(item["value"], dict):
                item["objectValue"] = item.pop("value")

    admin_info = data.get("administrativeInformation", {})
    pub_own = admin_info.get("publicationAndOwnership", {})
    if "other" in pub_own:
        pub_own["otherPAO"] = pub_own.pop("other")
        for item in pub_own["otherPAO"].get("anies", []):
            if isinstance(item, dict) and "value" in item and isinstance(item["value"], dict):
                item["objectValue"] = item.pop("value")

    exchanges = data.get("exchanges", {}).get("exchange", [])
    for exchange in exchanges:
        for fp in exchange.get("flowProperties", []):
            if "name" in fp:
                fp["nameFP"] = fp.pop("name")
            if "uuid" in fp:
                fp["uuidFP"] = fp.pop("uuid")

        if "exchange direction" in exchange:
            exchange["exchangeDirection"] = exchange.pop("exchange direction")

        if "other" in exchange:
            exchange["otherEx"] = exchange.pop("other")
            for item in exchange["otherEx"].get("anies", []):
                if isinstance(item, dict) and "value" in item and isinstance(item["value"], dict):
                    item["objectValue"] = item.pop("value")

        if "classification" in exchange:
            exchange["classificationEx"] = exchange.pop("classification")
            if "name" in exchange["classificationEx"]:
                exchange["classificationEx"]["nameClass"] = exchange["classificationEx"].pop("name")

        if "relativeStandardDeviation95In" in exchange:
            exchange.pop("relativeStandardDeviation95In")

    if "LCIAResults" in data:
        data["lciaResults"] = data.pop("LCIAResults")

    lcia_results = data.get("lciaResults", {}).get("LCIAResult", [])
    for result in lcia_results:
        if "other" in result:
            result["otherLCIA"] = result.pop("other")
            for item in result["otherLCIA"].get("anies", []):
                if isinstance(item, dict) and "value" in item and isinstance(item["value"], dict):
                    item["objectValue"] = item.pop("value")

        if "relativeStandardDeviation95In" in result:
            result.pop("relativeStandardDeviation95In")

    for removable_key in ("otherAttributes", "locations"):
        if removable_key in data:
            data.pop(removable_key)

    data = remove_raw_strings_in_anies(data)
    data = recursive_rename_uri(data)
    return data


def load_yaml_schema(file_path: Path) -> dict[str, Any]:
    with file_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def reorder_dict_keys(dct: dict[str, Any]) -> None:
    if "id" in dct:
        id_value = dct.pop("id")
        new_dict = {"id": id_value}
        new_dict.update(dct)
        dct.clear()
        dct.update(new_dict)


def generate_id_from_path(acc_path: str, prefix: str = "ilcd") -> str:
    return f"{prefix}:{acc_path}"


def get_suffix(item: Any, index: int) -> str:
    if isinstance(item, dict) and "module" in item:
        return f"module{str(item['module']).replace('-', '')}"
    return f"{index + 1:02d}"


def assign_ids_by_path(
    obj: Any,
    epd_uuid: str,
    acc_path: str,
    parent_is_list: bool,
    prefix: str = "ilcd",
) -> None:
    if isinstance(obj, dict) and "id" not in obj:
        obj["id"] = generate_id_from_path(f"{epd_uuid}_{acc_path}", prefix)
        reorder_dict_keys(obj)

    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "id":
                continue
            if isinstance(value, dict):
                new_acc = f"{acc_path}_{key}" if parent_is_list else key
                assign_ids_by_path(value, epd_uuid, new_acc, parent_is_list=False, prefix=prefix)
            elif isinstance(value, list):
                new_acc = f"{acc_path}_{key}"
                for index, item in enumerate(value):
                    suffix = get_suffix(item, index)
                    element_acc = f"{new_acc}_{suffix}"
                    assign_ids_by_path(item, epd_uuid, element_acc, parent_is_list=True, prefix=prefix)
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            suffix = get_suffix(item, index)
            new_acc = f"{acc_path}_{suffix}"
            assign_ids_by_path(item, epd_uuid, new_acc, parent_is_list=True, prefix=prefix)


def build_modified_json_docs(epd_records: list[dict[str, Any]], merged_schema_path: Path) -> dict[str, dict[str, Any]]:
    schema = load_yaml_schema(merged_schema_path)
    default_prefix = str(schema.get("default_prefix", "ilcd")).lower()

    modified_json_docs: dict[str, dict[str, Any]] = {}
    start_time = time.perf_counter()
    total_records = len(epd_records)
    for index, record in enumerate(epd_records, start=1):
        uuid_val = str(record["uuid"])
        document = copy.deepcopy(record["document"])
        transformed = transform_json(document)

        raw_uuid = transformed["processInformation"]["dataSetInformation"]["UUID"]
        epd_uuid = raw_uuid.replace("-", "")

        transformed["id"] = f"{default_prefix}:{epd_uuid}"
        for top_key, top_obj in transformed.items():
            if top_key in {"id", "version"}:
                continue
            if isinstance(top_obj, dict):
                top_obj["id"] = f"{default_prefix}:{epd_uuid}_{top_key}"
                reorder_dict_keys(top_obj)
                assign_ids_by_path(
                    top_obj,
                    epd_uuid=epd_uuid,
                    acc_path=top_key,
                    parent_is_list=False,
                    prefix=default_prefix,
                )
            elif isinstance(top_obj, list):
                for index, item in enumerate(top_obj):
                    suffix = get_suffix(item, index)
                    top_path = f"{top_key}_{suffix}"
                    assign_ids_by_path(
                        item,
                        epd_uuid=epd_uuid,
                        acc_path=top_path,
                        parent_is_list=True,
                        prefix=default_prefix,
                    )

        modified_json_docs[uuid_val] = transformed
        print_loop_progress("Transform JSON documents", index, total_records, start_time, interval=10)

    return modified_json_docs


def generate_graph_from_docs(
    docs_dict: dict[str, dict[str, Any]],
    schema_path: Path,
    validate_docs: bool = True,
) -> tuple[Graph, dict[str, dict[str, Any]]]:
    combined_graph = rdflib.Graph()
    schema_view = SchemaView(str(schema_path))
    validator = Validator(str(schema_path), strict=False) if validate_docs else None
    dumper = RDFLibDumper()
    failed_docs: dict[str, dict[str, Any]] = {}

    success_count = 0
    start_time = time.perf_counter()
    total_docs = len(docs_dict)
    for index, (uuid_val, json_doc) in enumerate(docs_dict.items(), start=1):
        yaml_wrapper = {"processDataSet": json_doc}

        if validator is not None:
            report = validator.validate(yaml_wrapper, "ProcessDataSet")
            if report.results:
                print(f"[VALIDATION] Issues for uuid={uuid_val}: {len(report.results)}")

        try:
            instance_obj = YAMLLoader().load(
                yaml_wrapper["processDataSet"], target_class=ProcessDataSet
            )
        except Exception as exc:
            print(f"[ERROR] Failed to load uuid={uuid_val} as ProcessDataSet: {exc}")
            failed_docs[uuid_val] = json_doc
            continue

        instance_graph = dumper.as_rdf_graph(instance_obj, schemaview=schema_view)
        combined_graph += instance_graph
        success_count += 1
        print_loop_progress("Generate base RDF documents", index, total_docs, start_time, interval=5)

    print(f"Loaded {success_count} ProcessDataSet instances into the base RDF graph")
    return combined_graph, failed_docs


def unify_ns_prefixes_graph(
    graph: Graph,
    base_uri: str = "https://example.org/ilcd/",
    old_ns_list: tuple[str, ...] = OLD_NS_LIST,
) -> Graph:
    new_graph = Graph()
    new_graph.bind("ilcd", URIRef(base_uri))
    new_graph.bind("xsd", URIRef("http://www.w3.org/2001/XMLSchema#"))

    def unify_uri(node: Any) -> Any:
        if not isinstance(node, URIRef):
            return node
        try:
            prefix, _, local = graph.compute_qname(node)
        except Exception:
            return node
        if prefix.startswith("ns") or f"{prefix}:" in old_ns_list or prefix in old_ns_list:
            return URIRef(base_uri + local)
        return node

    for subject, predicate, obj in graph:
        new_graph.add((unify_uri(subject), unify_uri(predicate), unify_uri(obj)))

    return new_graph


def parse_category_system(file_path: Path) -> tuple[ET.Element, dict[str, str]]:
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {"cat": "http://lca.jrc.it/ILCD/Categories"}
    if root.tag.endswith("CategorySystem") and root.get("name") == "OEKOBAU.DAT":
        category_system = root
    else:
        category_system = root.find(".//cat:CategorySystem[@name='OEKOBAU.DAT']", ns)
    if category_system is None:
        raise ValueError(f"CategorySystem 'OEKOBAU.DAT' not found in {file_path}")
    categories_elem = category_system.find("cat:categories", ns)
    if categories_elem is None:
        raise ValueError(f"No <categories> element found in {file_path}")
    return categories_elem, ns


def extract_target_categories(categories_elem: ET.Element, ns: dict[str, str]) -> tuple[dict[str, str], list[tuple[str, str]]]:
    targets: dict[str, str] = {}
    relations: list[tuple[str, str]] = []

    def traverse(elem: ET.Element, parent_id: str | None = None) -> None:
        cat_id = elem.get("id")
        cat_name = elem.get("name")
        if cat_id and cat_name:
            norm = cat_name.lower().strip()
            if norm in TARGET_CATEGORY_KEYS:
                targets[cat_id] = cat_name
                if parent_id is not None and parent_id in targets:
                    relations.append((parent_id, cat_id))
        for child in elem.findall("cat:category", ns):
            traverse(child, parent_id=cat_id)

    for child in categories_elem.findall("cat:category", ns):
        traverse(child)

    return targets, relations


def enrich_canonical_skos(graph: Graph, file_en: Path, file_de: Path) -> Graph:
    graph.bind("ilcd", ILCD)
    graph.bind("obd", OBD)
    graph.bind("skos", SKOS)

    categories_en_elem, ns_en = parse_category_system(file_en)
    categories_de_elem, ns_de = parse_category_system(file_de)
    targets_en, relations_en = extract_target_categories(categories_en_elem, ns_en)
    targets_de, _ = extract_target_categories(categories_de_elem, ns_de)

    merged_targets: dict[str, dict[str, str]] = {}
    for cat_id, en_label in targets_en.items():
        merged_targets[cat_id] = {"en": en_label}
    for cat_id, de_label in targets_de.items():
        merged_targets.setdefault(cat_id, {})
        merged_targets[cat_id]["de"] = de_label

    cat_scheme = OBD["OEKOBAU_DAT"]
    graph.add((cat_scheme, RDF.type, SKOS.ConceptScheme))
    graph.add((cat_scheme, SKOS.prefLabel, Literal("OEKOBAU.DAT", lang="en")))
    graph.add((cat_scheme, SKOS.prefLabel, Literal("OEKOBAU.DAT", lang="de")))

    for cat_id, labels in merged_targets.items():
        cat_uri = OBD["Category_" + cat_id.replace(".", "_")]
        graph.add((cat_uri, RDF.type, SKOS.Concept))
        if "en" in labels:
            graph.add((cat_uri, SKOS.prefLabel, Literal(labels["en"], lang="en")))
        if "de" in labels:
            graph.add((cat_uri, SKOS.prefLabel, Literal(labels["de"], lang="de")))
        graph.add((cat_uri, SKOS.inScheme, cat_scheme))

    for entry in graph.subjects(RDF.type, ILCD.ClassificationEntry):
        value = graph.value(entry, ILCD.value)
        if value is None:
            continue
        norm_value = str(value).lower().strip()
        if norm_value not in TARGET_CATEGORY_KEYS:
            continue
        for cat_id, labels in merged_targets.items():
            if (
                ("en" in labels and labels["en"].lower().strip() == norm_value)
                or ("de" in labels and labels["de"].lower().strip() == norm_value)
            ):
                cat_uri = OBD["Category_" + cat_id.replace(".", "_")]
                graph.add((entry, OBD.hasCanonicalCategory, cat_uri))
                break

    for parent_id, child_id in relations_en:
        if parent_id in merged_targets and child_id in merged_targets:
            parent_uri = OBD["Category_" + parent_id.replace(".", "_")]
            child_uri = OBD["Category_" + child_id.replace(".", "_")]
            graph.add((child_uri, SKOS.broader, parent_uri))
            graph.add((parent_uri, SKOS.narrower, child_uri))

    return graph


def find_top_epd_node_by_uuid(graph: Graph, epd_uuid: str) -> URIRef | None:
    uuid_literal = Literal(epd_uuid, datatype=LINKML_UUID)
    for dsi_node in graph.subjects(predicate=ILCD.UUID, object=uuid_literal):
        for pi_node in graph.subjects(predicate=ILCD.dataSetInformation, object=dsi_node):
            for epd_node in graph.subjects(predicate=ILCD.processInformation, object=pi_node):
                if isinstance(epd_node, URIRef):
                    return epd_node
    return None


def enrich_din(graph: Graph, din_assignments: dict[str, list[str]], din_csv_path: Path) -> Graph:
    graph.bind("din", DIN)

    used_codes = {code for cost_codes in din_assignments.values() for code in cost_codes}
    din_code_to_concept: dict[str, URIRef] = {}

    with din_csv_path.open("r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            nr = row["Nr"].strip()
            if nr not in used_codes:
                continue

            label_en = row["Cost group (CG)"].strip()
            notes_en = row["Notes"].strip()
            concept_uri = DIN[f"costgroup_{nr}"]

            graph.add((concept_uri, RDF.type, SKOS.Concept))
            graph.add((concept_uri, SKOS.prefLabel, Literal(label_en, lang="en")))
            graph.add((concept_uri, SKOS.note, Literal(notes_en, lang="en")))
            graph.add((concept_uri, SKOS.notation, Literal(nr)))
            din_code_to_concept[nr] = concept_uri

    start_time = time.perf_counter()
    total_assignments = len(din_assignments)
    for index, (uuid_val, cost_codes) in enumerate(din_assignments.items(), start=1):
        epd_node = find_top_epd_node_by_uuid(graph, uuid_val)
        if epd_node is None:
            raise ValueError(f"No top EPD node found in RDF graph for uuid={uuid_val}")

        for code in cost_codes:
            concept_uri = din_code_to_concept.get(code)
            if concept_uri is None:
                raise ValueError(f"Cost code {code} for uuid={uuid_val} not found in DIN CSV vocabulary")
            graph.add((epd_node, DIN.hasDIN276CostGroup, concept_uri))
        print_loop_progress("Attach DIN assignments", index, total_assignments, start_time, interval=10)

    for code_parent, concept_parent in din_code_to_concept.items():
        if not code_parent.endswith("0"):
            continue
        for code_child, concept_child in din_code_to_concept.items():
            if code_child == code_parent:
                continue
            if code_child.startswith(code_parent[:2]) and not code_child.endswith("0"):
                graph.add((concept_child, SKOS.broader, concept_parent))
                graph.add((concept_parent, SKOS.narrower, concept_child))

    din_scheme = DIN["DIN276"]
    graph.add((din_scheme, RDF.type, SKOS.ConceptScheme))
    graph.add((din_scheme, SKOS.prefLabel, Literal("DIN 276", lang="en")))
    graph.add((din_scheme, SKOS.note, Literal("DIN 276:2018-12 - Cost planning in building", lang="en")))
    for concept in din_code_to_concept.values():
        graph.add((concept, SKOS.inScheme, din_scheme))

    return graph


def integrate_bki_xml(graph: Graph, xml_file_path: Path) -> None:
    ET.register_namespace("", "https://www.bauteileditor.de")
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    ns = {"elca": "https://www.bauteileditor.de"}
    element_nodes = root.findall(".//elca:element", ns)
    start_time = time.perf_counter()
    total_elements = len(element_nodes)

    for index, element_node in enumerate(element_nodes, start=1):
        component_nodes = element_node.findall(".//elca:component", ns)
        has_transportbeton = any(
            "transportbeton" in comp.get("processConfigName", "").lower()
            for comp in component_nodes
        )
        if not has_transportbeton:
            print_loop_progress(
                f"Scan BKI elements ({xml_file_path.name})",
                index,
                total_elements,
                start_time,
                interval=250,
            )
            continue

        element_uuid = element_node.get("uuid", "unknown").replace("-", "")
        din_code = element_node.get("din276Code", "unknown")
        element_uri = BKI[f"element_{element_uuid}"]

        graph.add((element_uri, RDF.type, BKI.BKIElement))
        graph.add((element_uri, DIN.hasDIN276CostGroup, DIN[f"costgroup_{din_code}"]))

        elem_info = element_node.find(".//elca:elementInfo", ns)
        if elem_info is not None:
            name_node = elem_info.find("elca:name", ns)
            desc_node = elem_info.find("elca:description", ns)
            if name_node is not None and name_node.text:
                graph.add((element_uri, BKI.name, Literal(name_node.text.strip(), datatype=XSD.string)))
            if desc_node is not None and desc_node.text:
                graph.add((element_uri, BKI.description, Literal(desc_node.text.strip(), datatype=XSD.string)))

        for comp_node in component_nodes:
            process_config_uuid = comp_node.get("processConfigUuid", "").replace("-", "")
            layer_size = comp_node.get("layerSize", "")
            layer_size_str = layer_size.replace(".", "").ljust(3, "0")[:3]
            layer_uri = BKI[f"layer_{process_config_uuid}_{layer_size_str}"]

            process_config_name = comp_node.get("processConfigName", "")
            life_time = comp_node.get("lifeTime", "")

            graph.add((layer_uri, RDF.type, BKI.Layer))
            graph.add((element_uri, BKI.hasLayer, layer_uri))
            graph.add((layer_uri, BKI.processConfigName, Literal(process_config_name, datatype=XSD.string)))

            if life_time.isdigit():
                graph.add((layer_uri, BKI.lifeTime, Literal(int(life_time), datatype=XSD.integer)))
            else:
                graph.add((layer_uri, BKI.lifeTime, Literal(life_time, datatype=XSD.string)))

            try:
                layer_size_float = float(layer_size)
            except ValueError:
                graph.add((layer_uri, BKI.layerSize, Literal(layer_size, datatype=XSD.string)))
            else:
                graph.add((layer_uri, BKI.layerSize, Literal(layer_size_float, datatype=XSD.float)))
        print_loop_progress(
            f"Scan BKI elements ({xml_file_path.name})",
            index,
            total_elements,
            start_time,
            interval=250,
        )


def enrich_bki(graph: Graph, xml_paths: list[Path]) -> Graph:
    graph.bind("bki", BKI)
    graph.bind("din", DIN)
    total_files = len(xml_paths)
    for index, xml_path in enumerate(xml_paths, start=1):
        print(f"BKI source {index}/{total_files}: {xml_path.name}")
        integrate_bki_xml(graph, xml_path)
    return graph
