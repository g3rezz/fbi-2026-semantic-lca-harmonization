"""Thin command-line interface to the configured local pipeline."""
import argparse
import json
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description="FBI 2026 semantic ILCD harmonization")
    parser.add_argument("command", choices=["diagnose", "prepare", "categorize-materials", "normalize", "enrich", "build", "run", "generate-linkml"])
    parser.add_argument("--config", type=Path, help="Local pipeline configuration (not used by generate-linkml)")
    parser.add_argument("--retrieval-only", action="store_true", help="categorize-materials: retrieve candidates without an LLM call")
    parser.add_argument("--limit", type=int, help="categorize-materials: process only the first N source records")
    args = parser.parse_args(argv)
    if args.command != "generate-linkml" and args.config is None:
        parser.error("--config is required for pipeline commands")
    if args.command == "generate-linkml" and args.config is not None:
        parser.error("generate-linkml uses only packaged schemas; omit --config")
    if args.command != "categorize-materials" and (args.retrieval_only or args.limit is not None):
        parser.error("--retrieval-only and --limit are only supported by categorize-materials")
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be a positive integer")
    try:
        if args.command == "categorize-materials":
            from .categorization import categorize
            from .workflow import load_config
            config, resolve = load_config(args.config)
            result = categorize(config, resolve, retrieval_only=args.retrieval_only, limit=args.limit)
        elif args.command == "generate-linkml":
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
