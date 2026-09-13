# Material categorization reproducibility

This page records the historical notebook variants and retrieval benchmark behind the optional material-categorization stage. For the current method, see [the pipeline](pipeline.md#optional-model-assisted-material-categorization). For running it, see [the README](../README.md#optional-material-categorization) and [input configuration](input-data.md#optional-material-categorization).

## Notebook variants and reconstruction

The package reconstructs the Jina/EPDNorge branch of the study's material alignment. Applying it to other source cohorts is a new run, not a reproduction of the earlier IES embedding experiment.

The source evidence is [category matching](https://github.com/g3rezz/lca-data-harmonization-pipeline/blob/main/pipeline2/notebooks/p2_category_matching.ipynb), [vector-store creation](https://github.com/g3rezz/lca-data-harmonization-pipeline/blob/main/pipeline2/notebooks/p2_vector_store_creation.ipynb), and [model evaluation](https://github.com/g3rezz/lca-data-harmonization-pipeline/blob/main/pipeline2/notebooks/p2_model_evaluation.ipynb). There are material version differences. The current Jina notebook cell sets `k=20`, while the saved EPDNorge contexts and batch requests use 10 candidates and `o3-mini` with high reasoning effort. An earlier IES experiment uses `mxbai-embed-large`, a score window, and low reasoning effort. That variant is not silently mixed into this stage. The exact embedding revision used for the original decisions was not pinned.

The operational default follows the saved top-10 EPDNorge contexts, without a dynamic score-window filter. A run using the notebook cell's top-20 setting supplies a different candidate set to the selector. The selector retains the EPDNorge prompt and its character-for-character category constraint.

## Taxonomy, embeddings, and model revision

The configured English ÖKOBAUDAT XML supplies leaf categories in traversal order, with the full hierarchy joined by ` > `. The stage reports the derived leaf count. The aligned study taxonomy has 326 leaves, including a repeated path string that remains a separate index row as in the original. All paths fit within the original notebook's 150-character chunks, so each path is embedded intact. No taxonomy or vector store is distributed with the package.

Category paths and product queries use `SentenceTransformer.encode()` with `jinaai/jina-embeddings-v3`, trusted custom model code, and flash attention disabled. No task adapter, prompt prefix, or additional normalization argument is supplied. The model's own SentenceTransformer modules remain in effect. The notebook used CUDA and revision `main`. Configure an explicit revision for repeatable runs. CPU execution is supported explicitly, with possible numerical differences. Category vectors are cached locally by category paths and embedding settings, including the resolved model revision and library versions.

## L2 versus cosine

Retrieval uses FAISS `IndexFlatL2`: lower squared Euclidean distance is better. Although the notebook specified LangChain's `DistanceStrategy.COSINE`, its stored index and constructor use L2, without an extra vector-normalization step. The prompt score is `1 - distance`, not a calibrated probability or a cosine-similarity value. Audits retain both distance and score at full precision. The prompt shows scores to two decimals.

## Retrieval benchmark versus final selection

The reported **0.93 means 93 of 100 manually assigned categories occurred in the top-50 retrieved candidate set**. It is not final LLM classification accuracy. The reported mean rank, approximately 5.92, averages found categories. This manually classified retrieval benchmark is distinct from the 100-record ready-mix graph sample.

The evaluation notebook explores `k=10,20,30,40,50` and MMR weights; the reported comparison uses `lambda_mult=1.0` and `fetch_k=100`. The saved query log underlying the reported result contains `Product`, `LCA Method Details`, `Technological Applicability`, and `Technology Description`, in that order, including literal `nan` values from CSV loading for missing fields. The current notebook instead comments out the LCA-method line and loads missing fields as empty strings. Those query variants must not be treated as interchangeable.

The benchmark hit test compares lowercased first-100-character prefixes; its rank test compares those prefixes case-sensitively. These conventions differ from the operational categorization query and exact output validation. A retrieval-only operational run is therefore not, by itself, a reproduction of that benchmark. Reproduction requires matching benchmark inputs, taxonomy, query text, model revision, and retrieval/evaluation settings. Final LLM agreement must be measured separately.

## Conditions for exact reproduction

Each candidate-audit row contains UUID, extracted fields, exact query, embedding settings and resolved revision, index key, leaf count, `top_k`, ranked category paths, squared L2 distances, `1 - distance` scores, requested LLM model/effort, and selection status. Successful rows also contain the returned model identifier and `best_category`. Retrieval-only rows have no selection. A failed selection is retained for inspection, and the command does not publish a completed decisions file.

Reproducing the reported retrieval result requires the same:

- Manually classified 100-record benchmark and expected category labels, distinct from the 100-record ready-mix graph sample.
- English taxonomy, full leaf-path strings, traversal order, and repeated index row.
- Saved benchmark query text, field order, cleaning, and missing-value representation, including literal `nan` values. The operational query uses `Product`, `Classification`, `PCR`, `Description`, and `Applicability`; it is not the benchmark query.
- Embedding weights and custom model code at the resolved revision, library versions, device, and encoding settings. Pinning a revision makes a new run identifiable but does not establish which revision produced the original decisions, since that revision was not pinned.
- Retrieval and evaluation settings: squared L2 distances, the appropriate top-k depth, `lambda_mult=1.0`, `fetch_k=100`, and the benchmark's prefix matching and rank conventions.

The reported top-50 accuracy and mean rank are not guarantees for a different taxonomy, model revision, query, or shortlist depth. Local candidate files retain the exact queries, embedding settings and resolved revision, ranks, distances, scores, and selection details for comparison. Licensed source records, benchmark records, source-derived validation artifacts, and vector caches are not distributed with this repository. Keep them local under their applicable licenses. Validation tests are also local and ignored.

Retrieval reproduction does not establish final LLM category agreement. Comparing final selections requires the same product fields, candidate ordering, score formatting, prompt, model, and reasoning settings. Any comparison between reconstructed selections and historical decisions should therefore be reported separately with the exact model endpoint, model identifier, reasoning settings, sample, and agreement measure.
