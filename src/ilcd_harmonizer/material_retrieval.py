"""Leaf-path retrieval using the study's SentenceTransformer and FAISS behavior."""
from hashlib import sha256
from importlib.metadata import version
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
import xml.etree.ElementTree as ET

MODEL = "jinaai/jina-embeddings-v3"
NS = "{http://lca.jrc.it/ILCD/Categories}"


def leaf_categories(path):
    """Return full leaf paths in XML traversal order, without translating labels."""
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise ValueError(f"Invalid category XML: {exc}") from exc
    systems = [root] if root.tag == NS + "CategorySystem" else list(root.iter(NS + "CategorySystem"))
    paths = []

    def walk(element, parents):
        parts = parents + [element.get("name") or "Unnamed"]
        children = element.findall(NS + "category")
        if children:
            for child in children:
                walk(child, parts)
        else:
            paths.append(" > ".join(parts))

    for system in systems:
        if system.get("name") != "OEKOBAU.DAT":
            continue
        for group in system.findall(NS + "categories"):
            if group.get("dataType", "Process") == "Process":
                for category in group.findall(NS + "category"):
                    walk(category, [])
    if not paths:
        raise ValueError("No OEKOBAU.DAT Process leaf categories found in the configured English XML")
    return paths


class StudyEmbeddings:
    """Use encode() unchanged: no added task, query prefix, or normalization flag."""

    def __init__(self, settings):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError('Install the optional dependencies with python -m pip install -e ".[rag]"') from exc
        name = settings.get("model", MODEL)
        if name != MODEL:
            raise ValueError(f"The reconstructed embedding setup supports {MODEL}; no model substitution is automatic")
        revision = settings.get("revision", "main")
        device = settings.get("device", "cuda")
        self.model = SentenceTransformer(
            name, trust_remote_code=True, revision=revision, device=device,
            model_kwargs={"use_flash_attn": False},
            local_files_only=settings.get("local_files_only", False),
        )
        config = self.model[0].auto_model.config
        self.metadata = {
            "model": name, "revision": revision,
            "resolved_revision": getattr(config, "_commit_hash", None),
            "device": device, "encode_task": None, "use_flash_attn": False,
            "versions": {name: version(name) for name in ("sentence-transformers", "transformers", "torch")},
        }

    def embed_documents(self, texts):
        return self.model.encode(texts)

    def embed_query(self, text):
        return self.model.encode(text)


class CategoryIndex:
    """Cache category vectors without pickle and search with FAISS IndexFlatL2."""

    def __init__(self, paths, embeddings, cache_dir):
        try:
            import faiss
            import numpy as np
        except ImportError as exc:
            raise RuntimeError('Install the optional dependencies with python -m pip install -e ".[rag]"') from exc
        self.paths, self.embeddings = paths, embeddings
        signature = {"format": 1, "paths": paths, "embedding": embeddings.metadata, "metric": "squared_l2"}
        serialized = json.dumps(signature, sort_keys=True, ensure_ascii=False)
        self.cache_key = sha256(serialized.encode("utf-8")).hexdigest()
        cache = Path(cache_dir) / f"{self.cache_key}.npz"
        if cache.exists():
            with np.load(cache, allow_pickle=False) as saved:
                if saved["signature"].item() != serialized:
                    raise ValueError("Category embedding cache signature mismatch")
                vectors = saved["vectors"]
        else:
            vectors = np.asarray(embeddings.embed_documents(paths), dtype="float32")
        vectors = np.ascontiguousarray(vectors, dtype="float32")
        if vectors.ndim != 2 or vectors.shape[0] != len(paths) or not vectors.shape[1] or not np.isfinite(vectors).all():
            raise ValueError("Invalid category embeddings: expected one finite vector per leaf path")
        if not cache.exists():
            cache.parent.mkdir(parents=True, exist_ok=True)
            temporary = None
            try:
                with NamedTemporaryFile(dir=cache.parent, suffix=".tmp", delete=False) as stream:
                    temporary = Path(stream.name)
                    np.savez(stream, vectors=vectors, signature=serialized)
                os.replace(temporary, cache)
            finally:
                if temporary is not None:
                    temporary.unlink(missing_ok=True)
        self.index = faiss.IndexFlatL2(vectors.shape[1])
        self.index.add(vectors)

    def retrieve(self, query, top_k):
        import numpy as np
        if type(top_k) is not int or top_k < 1:
            raise ValueError("top_k must be a positive integer")
        vector = np.asarray(self.embeddings.embed_query(query), dtype="float32")
        if vector.shape != (self.index.d,) or not np.isfinite(vector).all():
            raise ValueError("Query embedding has an invalid dimension or nonfinite values")
        distances, indices = self.index.search(vector.reshape(1, -1), min(top_k, len(self.paths)))
        return [{"category": self.paths[int(index)], "rank": rank,
                 "distance": float(distance), "score": float(1 - distance)}
                for rank, (distance, index) in enumerate(zip(distances[0], indices[0]), 1)]
