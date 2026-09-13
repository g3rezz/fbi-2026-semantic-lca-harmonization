"""Regenerate the consolidated LinkML schema and its Python model modules."""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
from tempfile import NamedTemporaryFile, TemporaryDirectory

from linkml.generators.linkmlgen import LinkmlGenerator
from linkml.generators.pythongen import PythonGenerator

PACKAGE_DIR = Path(__file__).resolve().parent
ROOT_SCHEMA = "linkml_processDataSet_schema.yaml"
MERGED_SCHEMA = "linkml_ILCDmergedSchemas_schema.yaml"

# Shared definitions precede the component modules and the root model.
MODEL_MODULES = (
    "linkml_shared_definitions",
    "linkml_processInformation_schema",
    "linkml_modellingAndValidation_schema",
    "linkml_administrativeInformation_schema",
    "linkml_exchanges_schema",
    "linkml_lciaResults_schema",
    "linkml_processDataSet_schema",
)

_CLASS_OPTIONS = {
    "gen_slots": True,
    "gen_classvars": True,
    "mergeimports": True,
    "metadata": True,
    "genmeta": False,
}

# LCIA primitive names resolve to the runtime types, independently of local classes.
_RUNTIME_IMPORTS = {
    name: f"linkml_runtime.linkml_model.types.{name}"
    for name in ("Boolean", "String", "Integer", "Float", "dateTime")
}


def get_schema_directory() -> Path:
    """Locate the packaged modular YAML schema definitions."""
    return PACKAGE_DIR / "resources" / "schemas"


def generate_merged_schema(schema_dir: Path | None = None) -> str:
    """Return consolidated YAML using the gen-linkml merge/materialization options."""
    directory = Path(schema_dir) if schema_dir is not None else get_schema_directory()
    generator = LinkmlGenerator(
        str(directory / ROOT_SCHEMA),
        mergeimports=True,
        format="yaml",
        # gen-linkml enables both materializations by default.
        materialize_attributes=True,
        materialize_patterns=True,
    )
    schema = generator.schemaview.schema
    schema.source_file = ROOT_SCHEMA
    schema.source_file_date = None
    schema.source_file_size = None
    schema.generation_date = None
    return generator.serialize().rstrip() + "\n"


def generate_python_models(schema_dir: Path | None = None) -> dict[str, str]:
    """Return Python source by filename, retaining the per-module generator options.

    ProcessInformation uses explicit class/slot options. LCIAResults additionally
    maps primitive imports. Shared definitions and the remaining modules use the
    pinned PythonGenerator defaults, which retain relative component imports.
    """
    directory = Path(schema_dir) if schema_dir is not None else get_schema_directory()
    models = {}
    for module in MODEL_MODULES:
        options = {}
        if module in {"linkml_processInformation_schema", "linkml_lciaResults_schema"}:
            options.update(_CLASS_OPTIONS)
        if module == "linkml_lciaResults_schema":
            options["importmap"] = dict(_RUNTIME_IMPORTS)
        generator = PythonGenerator(str(directory / f"{module}.yaml"), **options)
        # Retain schema/license metadata but replace the dated heading with stable text.
        generator.schema.source_file = f"{module}.yaml"
        generator.schema.source_file_date = None
        generator.schema.source_file_size = None
        generator.schema.generation_date = None
        source = (
            f"# Generated from {module}.yaml by LinkML PythonGenerator.\n"
            "# Regenerate with: ilcd-harmonizer generate-linkml\n"
            + generator.serialize().lstrip("\n").rstrip() + "\n"
        )
        compile(source, f"{module}.py", "exec")
        models[f"{module}.py"] = source
    return models


def _check_model_imports(models: dict[str, str]) -> None:
    """Check relative imports in isolation before touching the installed models."""
    with TemporaryDirectory(prefix="linkml-model-check-") as temporary:
        package = Path(temporary) / "generated_models"
        package.mkdir()
        (package / "__init__.py").write_text("", encoding="utf-8")
        for name, source in models.items():
            (package / name).write_text(source, encoding="utf-8", newline="\n")
        result = subprocess.run(
            [sys.executable, "-B", "-c",
             "from generated_models.linkml_processDataSet_schema import ProcessDataSet; "
             "assert ProcessDataSet.__name__ == 'ProcessDataSet'"],
            cwd=temporary, capture_output=True, text=True,
        )
        if result.returncode:
            raise RuntimeError(f"Generated model imports failed:\n{result.stderr}")


def regenerate_linkml_artifacts() -> list[Path]:
    """Generate and validate all artifacts, then replace changed package files.

    All content is prepared before replacement. Each file is staged beside its
    destination and replaced atomically; unchanged files are left untouched.
    """
    merged = generate_merged_schema()
    models = generate_python_models()
    _check_model_imports(models)
    artifacts = {get_schema_directory() / MERGED_SCHEMA: merged}
    artifacts.update({PACKAGE_DIR / "_generated" / name: source for name, source in models.items()})
    artifacts[PACKAGE_DIR / "_generated" / "__init__.py"] = ""

    pending = []
    try:
        for destination, source in artifacts.items():
            content = source.encode("utf-8")
            if destination.is_file() and destination.read_bytes() == content:
                print(f"Unchanged: {destination.relative_to(PACKAGE_DIR)}")
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            print(f"Writing: {destination.relative_to(PACKAGE_DIR)}", flush=True)
            with NamedTemporaryFile(dir=destination.parent, prefix=".linkml-", suffix=".tmp", delete=False) as stream:
                pending.append((Path(stream.name), destination))
                stream.write(content)
        for temporary, destination in pending:
            os.replace(temporary, destination)
    finally:
        for temporary, _ in pending:
            temporary.unlink(missing_ok=True)
    return [destination for _, destination in pending]
