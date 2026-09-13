"""Paper-facing SHACL rule execution, separate from validation reports."""
from pathlib import Path

from pyshacl import validate
from rdflib import Graph


def classify_properties(graph: Graph, shapes_path: Path):
    shapes = Graph().parse(shapes_path, format="turtle")
    conforms, report, report_text = validate(
        graph,
        shacl_graph=shapes,
        advanced=True,
        iterate_rules=True,
        inference="rdfs",
        inplace=True,
    )
    # Do not merge a validation report into the scientific data graph.
    if not isinstance(report, Graph):
        raise RuntimeError(f"SHACL execution failed: {report}")
    return bool(conforms), report, report_text
