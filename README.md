# FBI 2026 semantic LCA harmonization

Environmental product records from different repositories use different classifications, property names, and data structures. This Python package harmonizes ILCD/ILCD+EPD records into an RDF knowledge graph with shared material, planning, and property concepts, while retaining each record's UUID, source repository, and source classifications.

This repository accompanies the Forum Bauinformatik 2026 paper **“Harmonizing and Querying Fragmented Environmental Data Repositories for Early-Phase Building Design”**. The package implements its semantic harmonization pipeline using ready-mix concrete records from ÖKOBAUDAT, IBU.data, EPDNorge, and the International EPD System (IES).

## Pipeline

```mermaid
flowchart TD
    A[Local ILCD / ILCD+EPD records] --> B[Configure local paths]

    B --> C{Prepare deterministic IES rules?}
    C -- Yes --> D[prepare]
    D --> E[Configure material_rules]
    C -- No --> F{Required material category inputs complete?}
    E --> F

    F -- Yes --> G[normalize]
    F -- No --> H[categorize-materials]
    H --> I[Configure generated material_decisions]
    I --> G

    G --> J[Provide DIN decisions]
    J --> K[enrich]
    K --> L[build]
    L --> M[graph.ttl]

    N[Optional: generate-linkml] --> O[Regenerate LinkML schema + Python models]
```

1. **Normalize and select records.** Apply repository-specific handling and identify ready-mix concrete through source classifications, deterministic material rules, and precomputed category decisions.
2. **Enrich semantics.** Align materials to the ÖKOBAUDAT taxonomy and associate DIN 276 potential application contexts. Include BKI links through DIN when configured.
3. **Construct the graph.** Transform JSON through LinkML, create RDF identifiers, and link records to shared SKOS concepts.
4. **Classify properties.** Execute SHACL rules for strength and density classes and serialize the harmonized graph as Turtle.

The repository focuses on semantic harmonization and graph construction. A [small SPARQL example](src/ilcd_harmonizer/resources/example.rq) illustrates cross-repository access to the resulting graph. See [the pipeline method](docs/pipeline.md) for the selection rules and graph structure.

## Installation

Create and activate the Conda environment:

```console
conda env create -f environment.yml
conda activate fbi-2026-lca
```

The environment lists the runtime pins from `pyproject.toml` and installs the package. Alternatively, use a Python 3.12 virtual environment:

```console
python -m venv .venv
# Activate .venv using your shell's activation command.
python -m pip install -e .
```

For optional model-assisted material categorization, additionally install:

```console
python -m pip install -e ".[rag]"
```

The core environment does not require these embedding, FAISS, or OpenAI dependencies. Categorization loads Jina model weights and custom model code locally, downloading them on first use if needed. Set `material_categorization.embedding.device: cpu` when CUDA is unavailable.

## Inputs and configuration

Supply local ILCD/ILCD+EPD JSONL records, the external ÖKOBAUDAT taxonomy and DIN vocabulary, and UUID-keyed material/DIN decisions for semantic enrichment. Deterministic IES categorization can run directly on prepared material fields. BKI resources are optional.

Copy [config.example.yaml](config.example.yaml) to `config.local.yaml`, keep the source entries you use, and replace the placeholder paths with your local files. The template contains no source records or semantic decisions. Relative paths resolve beside the configuration file. Keep runtime configurations and research inputs local.

`input.sources` identifies the repository records and source URIs. `material_decisions` and optional `material_rules` supply material categories; `din_decisions` supplies planning assignments. `resources` locates the required English/German taxonomy and DIN vocabulary, an optional separate normalization hierarchy, and optional BKI files. `output_dir` receives preparation artifacts and pipeline outputs. [Input data](docs/input-data.md) explains the configuration keys, formats, and stage requirements.

## Run

With prepared inputs and complete material/DIN decisions, configure the local paths and run:

```console
ilcd-harmonizer run --config CONFIG_FILE
```

Starting with compatible local repository records, prepare IES fields where needed, then provide or complete material decisions before normalization:

```console
ilcd-harmonizer prepare --config CONFIG_FILE
```

`prepare` extracts eligible IES material fields into `output_dir/ies-material-fields.csv`. Enable `material_rules` in your local configuration with that file's path to use deterministic categorization. Preparation requires only configured IES records and an output directory; it does not load decisions or external vocabularies. Skip it when using existing prepared fields or precomputed material decisions.

Continue in stages:

```console
ilcd-harmonizer normalize --config CONFIG_FILE
```

Supply UUID-keyed DIN decisions for the selected records in `normalized.jsonl`, then run:

```console
ilcd-harmonizer enrich --config CONFIG_FILE
ilcd-harmonizer build --config CONFIG_FILE
```

`run` executes `normalize`, `enrich`, and `build` in order; preparation and model-assisted material categorization are separate optional steps. Use the same configuration for the individual stages. `ilcd-harmonizer diagnose --config CONFIG_FILE` produces source diagnostics. `python -m ilcd_harmonizer` exposes the same commands. Precomputed UUID-keyed material and DIN assignments remain supported; `run` never calls an external model.

## Optional material categorization

Retrieval-augmented generation (RAG) maps product metadata to ÖKOBAUDAT material categories. Jina embeddings retrieve a top-10 shortlist of leaf categories; an LLM selects one listed category to produce a UUID-keyed material decision. Existing precomputed decisions remain supported, and `run` never invokes this stage automatically.

Install `.[rag]` as shown above. In your local configuration, supply `input.sources`, the English taxonomy at `resources.category_en`, and `output_dir`. Under `material_categorization`, choose `repositories` (default `[epdnorge]`), embedding settings, and candidate/decision output paths. This stage reads source records directly; it does not require the IES `prepare` CSV.

Inspect retrieval without an LLM or API key:

```console
ilcd-harmonizer categorize-materials --config CONFIG_FILE --retrieval-only --limit 10
```

For LLM selection, configure `material_categorization.llm.base_url` with an OpenAI-compatible HTTPS endpoint. The current implementation reads the API key from `RWTH_API_KEY` in the process environment. The endpoint must support the configured model (default `o3-mini`) and high reasoning effort. Keep credentials out of configuration files.

```console
ilcd-harmonizer categorize-materials --config CONFIG_FILE --limit 10
```

Choose a new candidate output path before moving from retrieval-only to selection; existing outputs are not overwritten. Remove `--limit` to process all records in the selected sources. Selection makes one request per record, without automatic retries.

Both modes write `material-candidates.jsonl`; successful selection also writes `material-decisions.jsonl`. Set `material_decisions` to the generated decisions path before `normalize`. DIN decisions are supplied separately.

See [configuration details](docs/input-data.md#optional-material-categorization), [the method](docs/pipeline.md#optional-model-assisted-material-categorization), and [reproducibility notes](docs/reproducibility.md).

Validation tests are kept local and are not distributed with this repository.

Regenerate the merged LinkML schema and Python models from the packaged modular schemas with `ilcd-harmonizer generate-linkml`. This command requires no runtime configuration or research inputs.

## Outputs

The configured output directory contains:

| File | Contents |
|---|---|
| `ies-material-fields.csv` | Local deterministic material-rule input produced only by `prepare`. |
| `material-candidates.jsonl` | Optional categorization audit: query, embedding settings, candidate ranks/scores, and selection status. |
| `material-decisions.jsonl` | UUID-keyed `best_category` decisions, written only after all requested selections succeed. |
| `graph.ttl` | Harmonized RDF graph, including source identifiers and semantic links. |
| `normalized.jsonl` | Selected, normalized source records. |
| `enriched.jsonl` | Normalized records with DIN context assignments. |
| `normalization-report.json` | Per-record acceptance and selection reasons. |
| `shacl-report.ttl` | SHACL report, separate from the data graph. |
| `run-summary.json` | Input/output counts, repository counts, property-class coverage, and conformance status. |
| `diagnostics.json` | Source/property/module counts produced by `diagnose`. |

Categorization also caches category vectors in `output_dir/material-index` by default. All candidate files, decisions, caches, source records, and generated study artifacts remain local and ignored by Git.

## Paper, data availability, and citation

<!-- Add the paper DOI here when available. -->

This implementation accompanies the FBI 2026 paper's contribution: a shared semantic representation that supports querying across heterogeneous environmental-data repositories. DIN assignments express potential application contexts.

The source environmental records and some external semantic resources used in the study are subject to their respective licenses and are not redistributed in this repository. The pipeline operates on compatible local inputs supplied by the user.

When using the software, cite the accompanying FBI 2026 paper and identify the software version or commit. Software citation: **Georgi Tsakov (2026), _FBI 2026 semantic LCA harmonization_, version 0.1.0**, [repository](https://github.com/g3rezz/fbi-2026-semantic-lca-harmonization).

Code is licensed under the [MIT license](LICENSE.md). Packaged schemas and generated models retain their CC-BY-4.0 notices; see [NOTICE](NOTICE) for attribution.
