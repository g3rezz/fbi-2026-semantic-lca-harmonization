"""Optional material decisions from the reconstructed Jina/EPDNorge RAG method."""
import json
import os
import re
from urllib.parse import urlsplit

from .inputs import load_records, write_jsonl
from .material_retrieval import CategoryIndex, StudyEmbeddings, leaf_categories
from .preparation import SYNONYMS

QUERY_FIELDS = ("Product", "Classification", "PCR", "Description", "Applicability")
PROMPT_FIELDS = QUERY_FIELDS + ("Flow Property Name", "Flow Property Mean Value", "Flow Property Reference Unit")
SYSTEM_PROMPT = """You are an expert in product categorization. The following product information comes from an Environmental Product Declaration (EPD).

Your task:
- Review the product details and the list of possible categories.
- Treat the numeric scores only as guidance—choose the category that best fits the product based on its description and applicability, even if it is not the top score.
- Do not simply pick the highest-scoring category.
- Use exactly one of the listed categories, matching its name character-for-character.
- Do not invent any new categories.
"""


def clean_metadata(text):
    """The RAG preparation retains Unicode; it is separate from IES regex preparation."""
    if not isinstance(text, str):
        return "N/A"
    text = re.sub(r"\s+", " ", text.strip().replace("\n", " ")).replace("&", "and")
    for key, value in SYNONYMS.items():
        text = text.replace(key, value)
    return re.sub(r"[®™©]", "", text)


def product_fields(record):
    """Extract the first multilingual values and first exchange/property, as in the study."""
    document = record["document"]
    process = document.get("processInformation", {})
    info = process.get("dataSetInformation", {})
    technology = process.get("technology", {})

    def text(values):
        return clean_metadata(values[0].get("value", "")) if values else ""

    classifications = info.get("classificationInformation", {}).get("classification", [])
    classification = " / ".join(item.get("value", "") for item in classifications[0].get("class", [])) if classifications else ""
    references = document.get("modellingAndValidation", {}).get("LCIMethodAndAllocation", {}).get("referenceToLCAMethodDetails", [])
    exchanges = document.get("exchanges", {}).get("exchange", [])
    properties = exchanges[0].get("flowProperties", []) if exchanges else []
    prop = properties[0] if properties else {}
    fields = {
        "Product": text(info.get("name", {}).get("baseName", [])),
        "Classification": classification,
        "PCR": text(references[0].get("shortDescription", [])) if references else "",
        "Description": text(technology.get("technologyDescriptionAndIncludedProcesses", [])),
        "Applicability": text(technology.get("technologicalApplicability", [])),
        "Flow Property Name": text(prop.get("name", [])),
        "Flow Property Mean Value": prop.get("meanValue", ""),
        "Flow Property Reference Unit": prop.get("referenceUnit", ""),
    }
    return {key: "N/A" if value is None or value == "" else value for key, value in fields.items()}


def build_query(fields):
    return "".join(f"{key}: {fields.get(key, 'N/A')}\n" for key in QUERY_FIELDS
                   if key == "Product" or fields.get(key, "N/A") != "N/A")


def selection_request(fields, candidates, settings):
    details = "\n".join(f"- {key}: {fields[key]}" for key in PROMPT_FIELDS
                        if fields.get(key) and fields[key] != "N/A")
    choices = "\n".join(f"- {row['category']} (score: {row['score']:.2f})" for row in candidates)
    prompt = ("Product Details:\n" + details + "\n\nPossible Categories:\n" + choices
              + "\n\nWhich category is best? Please respond in valid json format.")
    return {
        "model": settings.get("model", "o3-mini"),
        "reasoning_effort": settings.get("reasoning_effort", "high"),
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
        "response_format": {"type": "json_schema", "json_schema": {
            "name": "BestCategoryResponse", "strict": True,
            "schema": {"type": "object", "title": "BestCategoryResponse",
                       "properties": {"best_category": {"type": "string", "title": "Best Category"}},
                       "required": ["best_category"], "additionalProperties": False},
        }},
    }


def validate_selection(content, candidates):
    try:
        result = json.loads(content)
    except (TypeError, json.JSONDecodeError) as exc:
        raise ValueError("Material selector returned malformed JSON") from exc
    if not isinstance(result, dict) or set(result) != {"best_category"} or not isinstance(result["best_category"], str):
        raise ValueError("Material selector must return exactly one string best_category")
    if result["best_category"] not in {row["category"] for row in candidates}:
        raise ValueError("Material selector returned a category outside the supplied candidate list")
    return result["best_category"]


def openai_client(settings):
    if settings.get("provider", "openai") != "openai":
        raise ValueError("Only the OpenAI-compatible selection interface is supported")
    key = os.environ.get("RWTH_API_KEY")
    if not key:
        raise ValueError("Set RWTH_API_KEY in the environment before LLM selection, or use --retrieval-only")
    url = settings.get("base_url", "")
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("material_categorization.llm.base_url must be an explicit HTTPS endpoint without credentials")
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError('Install the optional dependencies with python -m pip install -e ".[rag]"') from exc
    return OpenAI(api_key=key, base_url=url, max_retries=0, timeout=120.0)


def select_category(client, fields, candidates, settings):
    try:
        response = client.chat.completions.create(**selection_request(fields, candidates, settings))
    except Exception as exc:
        # Do not echo an SDK/server exception that could contain credentials or source text.
        raise RuntimeError(f"Material selection request failed ({type(exc).__name__}); no automatic retry") from None
    if len(response.choices) != 1:
        raise ValueError("Material selector did not return exactly one completion")
    choice = response.choices[0]
    if choice.finish_reason != "stop" or getattr(choice.message, "refusal", None):
        raise ValueError("Material selection was refused or incomplete")
    category = validate_selection(choice.message.content, candidates)
    return category, response.model


def categorize(config, resolve, *, retrieval_only=False, limit=None):
    settings = config.get("material_categorization", {})
    top_k = settings.get("top_k", 10)
    if type(top_k) is not int or top_k < 1:
        raise ValueError("material_categorization.top_k must be a positive integer")
    if limit is not None and (type(limit) is not int or limit < 1):
        raise ValueError("limit must be a positive integer")
    repositories = settings.get("repositories", ["epdnorge"])
    if not isinstance(repositories, list) or not repositories or any(name not in {"epdnorge", "ies", "ibu", "oekobaudat"} for name in repositories):
        raise ValueError("material_categorization.repositories must list supported repository identifiers")
    sources = [source for source in config["input"]["sources"] if source.get("repository") in repositories]
    if not sources:
        raise ValueError("No input sources match material_categorization.repositories")
    records = load_records({**config, "input": {**config["input"], "sources": sources}}, resolve)
    if limit is not None:
        records = records[:limit]
    if not records:
        raise ValueError("No records available for material categorization")
    taxonomy = resolve(config["resources"]["category_en"])
    paths = leaf_categories(taxonomy)
    output = resolve(config["output_dir"])
    outputs = settings.get("output", {})
    candidates_path = resolve(outputs["candidates"]) if "candidates" in outputs else output / "material-candidates.jsonl"
    decisions_path = resolve(outputs["decisions"]) if "decisions" in outputs else output / "material-decisions.jsonl"
    protected = {resolve(source["path"]) for source in sources} | {taxonomy}
    if candidates_path == decisions_path or candidates_path in protected or decisions_path in protected:
        raise ValueError("Categorization output paths must be distinct from each other and from source/taxonomy inputs")
    if candidates_path.exists() or (not retrieval_only and decisions_path.exists()):
        raise ValueError("Categorization output already exists; choose new output paths to preserve earlier decisions and audits")
    llm = settings.get("llm", {})
    client = None if retrieval_only else openai_client(llm)
    decisions = []
    try:
        embeddings = StudyEmbeddings(settings.get("embedding", {}))
        cache_dir = resolve(settings["cache_dir"]) if "cache_dir" in settings else output / "material-index"
        index = CategoryIndex(paths, embeddings, cache_dir)
        candidates_path.parent.mkdir(parents=True, exist_ok=True)
        with candidates_path.open("x", encoding="utf-8") as audit:
            for record in records:
                fields = product_fields(record)
                query = build_query(fields)
                candidates = index.retrieve(query, top_k)
                row = {"uuid": record["uuid"], "query_fields": fields, "query": query,
                       "embedding": embeddings.metadata, "index_key": index.cache_key,
                       "leaf_categories": len(paths), "top_k": top_k, "metric": "squared_l2",
                       "candidates": candidates, "llm_model": None if retrieval_only else llm.get("model", "o3-mini"),
                       "reasoning_effort": None if retrieval_only else llm.get("reasoning_effort", "high"),
                       "best_category": None, "status": "retrieval_only"}
                if client is not None:
                    try:
                        selected, returned_model = select_category(client, fields, candidates, llm)
                        row.update(best_category=selected, returned_llm_model=returned_model, status="selected")
                        decisions.append({"uuid": record["uuid"], "best_category": selected})
                    except (ValueError, RuntimeError) as exc:
                        row.update(status="selection_failed", error=str(exc))
                        audit.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
                        raise
                audit.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
                audit.flush()
        if not retrieval_only:
            write_jsonl(decisions_path, decisions)
    finally:
        if client is not None:
            client.close()
    return {"records": len(records), "leaf_categories": len(paths), "top_k": top_k,
            "retrieval_only": retrieval_only, "candidates": str(candidates_path),
            "decisions": None if retrieval_only else str(decisions_path)}
