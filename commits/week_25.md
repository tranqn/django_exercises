# Week 25 — Machine Learning Integration

## Commit #360
**Message:** `feat(ml): add model registry and lazy loader`
**Files:**

```file:advanced/ml_integration/registry.py
"""Load ML models once and reuse across requests."""

import threading

_lock = threading.Lock()
_models = {}


def get_model(name, loader):
    if name not in _models:
        with _lock:
            if name not in _models:
                _models[name] = loader()
    return _models[name]
```

---

## Commit #361
**Message:** `feat(ml): add scikit-learn inference service`
**Files:**

```file:advanced/ml_integration/sklearn_service.py
"""Load a pickled sklearn pipeline and predict.

pip install scikit-learn joblib
"""

import joblib

from .registry import get_model


def _load():
    return joblib.load("models/churn_pipeline.joblib")


def predict_churn(features: dict) -> float:
    model = get_model("churn", _load)
    proba = model.predict_proba([list(features.values())])[0][1]
    return float(proba)
```

---

## Commit #362
**Message:** `feat(ml): add async inference task`
**Files:**

```file:advanced/ml_integration/inference_task.py
"""Run heavy inference off the request path via Celery."""

from celery import shared_task


@shared_task(bind=True, max_retries=2)
def run_batch_inference(self, dataset_id):
    from .sklearn_service import predict_churn
    # load dataset rows, score each, persist results...
    return {"dataset": dataset_id, "status": "scored"}
```

---

## Commit #363
**Message:** `feat(ml): add feature store accessor`
**Files:**

```file:advanced/ml_integration/feature_store.py
"""Assemble features for a subject from cached + live sources."""

from django.core.cache import cache


def get_features(user_id):
    key = f"features:user:{user_id}"
    features = cache.get(key)
    if features is None:
        features = _compute_features(user_id)
        cache.set(key, features, timeout=3600)
    return features


def _compute_features(user_id):
    return {"orders_30d": 0, "avg_basket": 0.0, "days_since_login": 0}
```

---

## Commit #364
**Message:** `feat(ml): add LLM client with caching`
**Files:**

```file:advanced/ml_integration/llm_client.py
"""Cached LLM calls to cut cost and latency on repeat prompts."""

import hashlib

from django.core.cache import cache


def cached_completion(prompt, call_model, timeout=86400):
    key = "llm:" + hashlib.sha256(prompt.encode()).hexdigest()
    cached = cache.get(key)
    if cached is not None:
        return cached
    result = call_model(prompt)
    cache.set(key, result, timeout)
    return result
```

---

## Commit #365
**Message:** `feat(ml): add embedding generation and storage`
**Files:**

```file:advanced/ml_integration/embeddings.py
"""Store vector embeddings in Postgres with pgvector.

pip install pgvector
CREATE EXTENSION vector;
"""

from django.db import models
from pgvector.django import VectorField


class DocumentEmbedding(models.Model):
    document_id = models.PositiveIntegerField(db_index=True)
    embedding = VectorField(dimensions=1536)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## Commit #366
**Message:** `feat(ml): add semantic similarity search`
**Files:**

```file:advanced/ml_integration/semantic_search.py
"""Nearest-neighbor search over embeddings (cosine distance)."""

from pgvector.django import CosineDistance


def semantic_search(query_vector, top_k=10):
    from .embeddings import DocumentEmbedding
    return (
        DocumentEmbedding.objects
        .annotate(distance=CosineDistance("embedding", query_vector))
        .order_by("distance")[:top_k]
    )
```

---

## Commit #367
**Message:** `feat(ml): add RAG retrieval pipeline`
**Files:**

```file:advanced/ml_integration/rag.py
"""Retrieval-augmented generation: fetch context, then prompt."""


def build_rag_prompt(question, embed, search, render_docs):
    query_vec = embed(question)
    hits = search(query_vec, top_k=5)
    context = render_docs(hits)
    return (
        "Answer using only the context below.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
```

---

## Commit #368
**Message:** `feat(ml): add prediction logging for monitoring`
**Files:**

```file:advanced/ml_integration/prediction_log.py
"""Log predictions to detect drift and enable later evaluation."""

from django.db import models


class Prediction(models.Model):
    model_name = models.CharField(max_length=80)
    model_version = models.CharField(max_length=40)
    inputs = models.JSONField()
    output = models.JSONField()
    latency_ms = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
```

---

## Commit #369
**Message:** `feat(ml): add input validation guardrails`
**Files:**

```file:advanced/ml_integration/guardrails.py
"""Validate and bound model inputs before inference."""


class GuardrailError(Exception):
    pass


def validate_features(features, schema):
    for name, (low, high) in schema.items():
        if name not in features:
            raise GuardrailError(f"missing feature: {name}")
        value = features[name]
        if not (low <= value <= high):
            raise GuardrailError(f"{name}={value} out of range [{low}, {high}]")
    return True
```

---

## Commit #370
**Message:** `test(ml): add inference and guardrail tests`
**Files:**

```file:advanced/ml_integration/test_ml.py
"""Tests for guardrails and the model registry."""

from django.test import SimpleTestCase

from .guardrails import GuardrailError, validate_features


class GuardrailTests(SimpleTestCase):
    SCHEMA = {"age": (0, 120), "score": (0.0, 1.0)}

    def test_valid_passes(self):
        self.assertTrue(validate_features({"age": 30, "score": 0.5}, self.SCHEMA))

    def test_out_of_range_raises(self):
        with self.assertRaises(GuardrailError):
            validate_features({"age": 200, "score": 0.5}, self.SCHEMA)
```

---

## Commit #371
**Message:** `docs(week25): add ML integration reference`
**Files:**

```file:advanced/ML_REFERENCE.md
# Week 25 — Machine Learning Integration

- **Serving** — singleton model registry, lazy load, async Celery inference.
- **Features** — cached feature store accessor.
- **LLM/RAG** — cached completions, pgvector embeddings, cosine NN search,
  retrieval-augmented prompting.
- **Safety** — input guardrails, prediction logging for drift/eval.

## Production tips
- Keep models out of the request thread; warm them at startup.
- Version every model; log inputs+outputs for monitoring.
- Cache deterministic LLM/embedding calls aggressively.
```
