"""Thin command-line interface to the configured local pipeline."""
import argparse
import json
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description="FBI 2026 semantic ILCD harmonization")
    parser.add_argument("command", choices=["diagnose", "prepare", "normalize", "enrich", "build", "run", "generate-linkml"])
    parser.add_argument("--config", type=Path, help="Local pipeline configuration (not used by generate-linkml)")
    args = parser.parse_args(argv)
    if args.command != "generate-linkml" and args.config is None:
        parser.error("--config is required for pipeline commands")
    if args.command == "generate-linkml" and args.config is not None:
        parser.error("generate-linkml uses only packaged schemas; omit --config")
    try:
        if args.command == "generate-linkml":
            from .schema_generation import regenerate_linkml_artifacts
            written = regenerate_linkml_artifacts()
            result = {"artifacts_written": len(written)}
        else:
            from .workflow import execute
            result = execute(args.command, args.config)
    except (ValueError, KeyError, OSError, RuntimeError) as exc:
        parser.exit(2, f"Pipeline error: {exc}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
