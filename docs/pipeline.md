# Semantic harmonization pipeline

The pipeline aligns ILCD/ILCD+EPD records from four repositories to shared material, planning, and property concepts. Its ready-mix concrete case study connects heterogeneous source descriptions in a single queryable RDF graph.

## Source normalization and selection

| Source | Ready-mix selection and normalization |
|---|---|
| ÖKOBAUDAT / IBU.data | Select the source's classification system, a `Beton` classification, a strength or density property, and a `Cxx/yy` product name. Append `yy` as compressive strength in MPa to the first exchange. |
| International EPD System (IES) | Select an exact ready-mix material category and separate strength/density properties. Standardize property names and unit labels, append the ÖKOBAUDAT category path, and remove separate A1/A2/A3 entries. |
| EPDNorge | Select an exact ready-mix category, a geographic location, and first-exchange strength/density properties after extraction from the product name and volume/mass fields. Aggregate A1/A2/A3 and append the ÖKOBAUDAT category path. |

Source classifications remain in each record. ÖKOBAUDAT and IBU.data use classification-system names `OEKOBAU.DAT` and `IBUCategories`, respectively. Repository identity is supplied independently of these classifications.

The property handling is specific: `Cxx/yy` supplies the second value; EPDNorge `Bxx` supplies `xx`. Density can be derived when the first exchange describes volume equal to 1 m³ and a mass value. Unit-label normalization does not perform numeric unit conversion. EPDNorge module aggregation treats nonnumeric values as zero and emits a zero aggregate when individual modules are present. Values are combined without additional scenario grouping. Users should supply records appropriate to these conventions.

All accepted records are included by default. An optional ordered `selection_uuids` list selects a subset. Duplicate source UUIDs are rejected to keep record identity unambiguous.

## Material categorization

Deterministic IES rules classify prepared product names, technology descriptions, applicability, and flow-property fields. The ordered predicates distinguish admixtures, aggregates, volume-based concrete, cement, ready-mix products, precast products, and other materials. Rule order and Boolean precedence determine the result.

Model-assisted cases use precomputed UUID-keyed category decisions supplied as normal inputs. Selection requires the exact path:

```text
Mineral building products > Mortar and Concrete > Ready mixed concrete
```

If a rule result and an input decision for the same UUID disagree, the pipeline reports a conflict. Records missing a required material decision appear in the normalization report with the rejection reason.

## Shared material and planning concepts

ÖKOBAUDAT categories form a SKOS concept scheme with English/German labels and broader/narrower links. The concrete branch provides canonical concepts for source classification entries, connected by `obd:hasCanonicalCategory`. Matching uses category labels and the configured taxonomy identifiers.

Precomputed DIN decisions associate each selected record with cost-group concepts through `din:hasDIN276CostGroup`. The concepts include vocabulary labels, notation, and applicable hierarchy links. These assignments express **potential application contexts**, not definitive building-element assignments. Each selected record requires a DIN decision; vocabulary entries must cover its assigned codes.

When BKI XML resources are configured, the pipeline adds elements containing Transportbeton, their component layers, and DIN links. Shared DIN concepts connect the EPD and BKI contexts.

## LinkML and RDF construction

The modular YAML files in `src/ilcd_harmonizer/resources/schemas/` are the schema source. The root `linkml_processDataSet_schema.yaml` imports the shared definitions and the ProcessInformation, ModellingAndValidation, AdministrativeInformation, Exchanges, and LCIAResults components. They define the model explicitly; the pipeline does not infer schemas from EPD instances or ILCD XSD.

```text
modular LinkML YAML schemas
        ↓
merged ILCD LinkML schema
        ↓
generated Python model classes
        ↓
normalized ILCD/ILCD+EPD instances
        ↓
LinkML validation/loading
        ↓
RDF serialization
```

Run `ilcd-harmonizer generate-linkml` to recreate `linkml_ILCDmergedSchemas_schema.yaml` and the seven Python model modules in `src/ilcd_harmonizer/_generated/`. The merged schema resolves imports and materializes induced attributes and patterns. PythonGenerator builds the model modules from their corresponding modular schemas, retaining shared definitions and relative imports; normalized records are instances of those models.

Generation uses the pinned LinkML version, keeps the component-specific generator settings and LCIA runtime type mappings, and produces stable content without timestamps or local paths. The command prepares all artifacts and checks model imports before replacing changed files, reporting each destination. The generated files are written at their existing package locations, so the installed package directory must be writable.

JSON keys and nested structures are adapted to the packaged LinkML schemas. The root RDF identifier derives from the source UUID; nested identifiers use structural paths and list/module identifiers. LinkML models serialize the adapted records to RDF, and graph terms are consolidated under the package's ILCD namespace.

Graph construction reads the consolidated schema for identifier preparation and the root schema for validation and RDF serialization. Regeneration retains these roles and the existing model imports.

The graph retains source UUIDs, source classifications, and available source references. Each EPD also has a `dcterms:source` link to its configured repository URI. These source links keep records traceable alongside the harmonized semantic links.

Useful graph paths are:

| Information | Relation or path from the EPD |
|---|---|
| UUID | `ilcd:processInformation / ilcd:dataSetInformation / ilcd:UUID` |
| Repository | `dcterms:source` |
| Material | Classification entries linked through `obd:hasCanonicalCategory` |
| Application context | `din:hasDIN276CostGroup` |
| Strength class | `cc:hasStrengthClassification` |
| Density class | `cc:hasWeightClassification` |

The [example query](../src/ilcd_harmonizer/resources/example.rq) combines these paths across repositories.

## SHACL property classification

SHACL SPARQL rules classify numeric material-property values using these intervals:

| Property | Low/light | Medium/normal | High/heavy |
|---|---|---|---|
| Strength, MPa | `<25` | `25–40` inclusive | `>40` |
| Density, kg/m³ | `<2000` | `2000–2600` inclusive | `>2600` |

Execution enables advanced rules, iterative rule application, and RDFS inference. The resulting graph contains the class links, SKOS class concepts, and RDFS entailments. Executable predicates define the intervals; some descriptive notes in the distributed rule resource use less precise boundaries.

The Turtle graph is the main output. A separate SHACL report and compact run summary report execution and class coverage. LinkML diagnostics do not reject records by themselves; model-loading failures stop graph construction. SHACL conformance for these classification rules is not a general completeness check, so the summary reports actual class coverage.
