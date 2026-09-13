# Input data

The pipeline uses compatible local source records, precomputed semantic decisions where required, and external semantic resources. A local runtime configuration identifies these inputs and the output destination.

## Configuration

Copy [config.example.yaml](../config.example.yaml) to an ignored local file such as `config.local.yaml`. Keep only the source entries you use and supply your own files. All relative paths resolve against the configuration file's directory.

| Key | Meaning and requirement |
|---|---|
| `input.sources` | List of local sources. Each entry requires `repository`, `path`, and `repository_uri`. |
| `input.sources[].format` | Optional `jsonl` (default) or `sqlite`. SQLite also requires `base_uri`, the exact source key stored in the database. |
| `input.mode` | Optional `raw` (default) or `normalized`. Use `normalized` only for records already processed according to the pipeline's normalization rules. |
| `material_decisions` | Path or list of paths to UUID-keyed material decisions. Required for IES/EPDNorge records whose categories are not supplied by deterministic rules. Omit when unused. |
| `material_rules` | Optional path to the prepared IES CSV consumed by deterministic material rules. |
| `din_decisions` | Path or list of paths to DIN decisions covering every selected record; required for `enrich` and therefore `run`. |
| `resources.category_en` | English taxonomy used for canonical linking and, by default, normalization. |
| `resources.category_de` | German taxonomy for canonical linking. Required by `build`. |
| `resources.category_api` | Optional separate taxonomy hierarchy for normalization; defaults to `category_en`. |
| `resources.din_csv` | DIN vocabulary required by `build`. |
| `resources.bki_xml` | Optional list of BKI XML paths; omit or use `[]` to omit BKI enrichment. |
| `selection_uuids` | Optional explicit ordered subset of accepted UUIDs. Duplicates or unaccepted UUIDs cause an error. Omit to retain all accepted records. |
| `output_dir` | Local destination for preparation and stage outputs; required for all configured commands. |

`prepare` reads only configured IES sources and writes `ies-material-fields.csv`; decisions and external vocabularies are not needed for that command. `diagnose` reads the configured sources. `normalize` reads source records, applicable material inputs, and the normalization taxonomy for raw inputs. `enrich` reads `normalized.jsonl` and DIN decisions. `build` reads `enriched.jsonl`, `normalization-report.json`, and the configured semantic resources. Keep the same configuration and output directory between stages.

With prepared inputs and complete decisions, run `ilcd-harmonizer run --config CONFIG_FILE`. Otherwise, prepare IES fields where needed, supply material decisions, run `normalize`, supply DIN decisions for its selected UUIDs, then run `enrich` and `build`. The [README](../README.md#run) gives the commands. Missing required files, malformed or conflicting decisions, and missing DIN assignments are pipeline errors; existing normalization rejection reasons remain in `normalization-report.json`.

## Repository records

Each input source supplies its repository identity, local records, and an absolute HTTP(S) source URI. Supported repositories are ÖKOBAUDAT (`oekobaudat`), IBU.data (`ibu`), EPDNorge (`epdnorge`), and the International EPD System (IES, `ies`).

JSONL is the default: one ILCD/ILCD+EPD API JSON document per line, or a wrapper containing a `document` object. Each document requires `processInformation.dataSetInformation.UUID`. The representation uses multilingual arrays, source classifications, exchange/material-property arrays, and `other.anies` module extensions. Supply the complete applicable document in that representation; an arbitrary XML or JSON export is not interchangeable with it.

Wrappers may include `uuid`, `id`, `epd_name`, and `classificationSys`. A wrapper UUID must agree with the document UUID. The `source_classification_system` field can supply the repository's classification-system metadata when it differs from the first classification in the document. Original classifications remain inside the document.

SQLite input is also supported. It requires `epd_documents(uuid, document)` and `epd_metadata(uuid, base_uri, classification_system)` tables. Records are selected by their stored source key and associated with a repository URI. The connection is read-only and skips empty/unparseable document rows.

## Semantic decisions

Supply material decisions as JSONL with `uuid` and `best_category`:

```json
{"uuid": "<source-record-uuid>", "best_category": "Mineral building products > Mortar and Concrete > Ready mixed concrete"}
```

Material decisions are needed for IES and EPDNorge unless a deterministic rule supplies the IES result. Exact category strings determine ready-mix selection.

Supply DIN decisions as JSONL with `uuid` and `cost_group_codes`:

```json
{"uuid": "<source-record-uuid>", "cost_group_codes": ["322", "331"]}
```

Codes are three-digit strings and express potential application contexts. Each selected record needs a decision. Decisions can be supplied in one or more files. Identical duplicate decisions are combined; conflicting decisions are rejected. Extra UUIDs outside the selected input set are ignored.

Precomputed decisions can be generated externally, including through the model-assisted methods used in the study. The pipeline consumes their semantic assignments directly.

## Deterministic IES rules

The deterministic material rules consume prepared CSV fields with these columns:

```text
UUID,Product Name,Technology Description,Technological Applicability,
Flow Property Name,Flow Property Mean Value,Flow Property Reference Unit
```

Product/technology text and flow fields feed the ordered regex classifier. Flow mean values use text such as `1` or `1.0`, and the volume reference unit is `m3`. Supply prepared fields consistent with the records being classified. A UUID can appear in both the CSV and material-decision JSONL only when their categories agree.

To prepare these fields from compatible local IES records, run `ilcd-harmonizer prepare --config CONFIG_FILE`. Set `material_rules` to the resulting CSV path (for example, `outputs/ies-material-fields.csv`). This step is optional when prepared fields or precomputed material decisions are already available. Other sources are not included in this CSV.

Preparation uses the first base-name value, the first technology-description and applicability values, and the first exchange's first flow property. It does not choose a preferred language or combine translations. Text cleaning trims and collapses whitespace, replaces `&` with `and`, removes characters outside the retained ASCII letters, numbers, punctuation, and separators, and applies the ordered unit-word substitutions. Product and technology text retain case; the first classification label is lowercased for eligibility. Flow mean values and reference-unit strings are copied directly.

Eligible classification labels after cleaning are `construction products, infrastructure and buildings`, `construction products`, or an empty label. These preparation rules select material-rule inputs; the existing source-specific normalization still determines which records enter the graph. The command reports preparation counts and the output path without changing the pipeline reports. Generated CSVs contain source-derived data and must remain local and ignored, together with the source records and decisions.

## External semantic resources

| Resource | Required content |
|---|---|
| Material hierarchy | ÖKOBAUDAT XML category hierarchy containing the exact English material path. |
| Multilingual taxonomy | English and German ÖKOBAUDAT XML category labels aligned by the same IDs for SKOS construction. The English file may also supply the material hierarchy. |
| DIN vocabulary | CSV with `Nr`, `Cost group (CG)`, and `Notes` columns covering all assigned DIN codes. |
| BKI context | Optional Bauteileditor XML files containing element/component structures and DIN codes. |

Taxonomy XML uses the `http://lca.jrc.it/ILCD/Categories` namespace and `OEKOBAU.DAT` category system. The hierarchy used for normalization must contain the exact material path above. BKI XML uses the `https://www.bauteileditor.de` namespace; these resources are needed only when BKI context is configured.

The source environmental records and some external semantic resources used in the study are subject to their respective licenses and are not redistributed in this repository. The pipeline operates on compatible local inputs supplied by the user. Keep outputs subject to the same applicable input/resource restrictions.
