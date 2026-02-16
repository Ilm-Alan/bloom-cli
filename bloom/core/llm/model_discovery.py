from __future__ import annotations

import json
import logging
import os
from pathlib import Path
import time
from typing import Any

import httpx

from bloom.core.config import ModelConfig

logger = logging.getLogger(__name__)

MODELS_API_URL = "https://gen.pollinations.ai/text/models"
CACHE_TTL_SECONDS = 3600  # 1 hour


def _get_cache_path() -> Path:
    from bloom.core.paths.global_paths import BLOOM_HOME

    return BLOOM_HOME.path / "models_cache.json"


def _load_cache() -> list[dict[str, Any]] | None:
    cache_path = _get_cache_path()
    if not cache_path.exists():
        return None
    try:
        data = json.loads(cache_path.read_text())
        if time.time() - data.get("timestamp", 0) > CACHE_TTL_SECONDS:
            return None
        return data.get("models")
    except (json.JSONDecodeError, OSError, KeyError):
        return None


def _save_cache(models: list[dict[str, Any]]) -> None:
    cache_path = _get_cache_path()
    try:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps({"timestamp": time.time(), "models": models}))
    except OSError:
        pass


def fetch_models(*, force_refresh: bool = False) -> list[dict[str, Any]]:
    """Fetch available models from Pollinations /text/models API, with caching."""
    if not force_refresh:
        cached = _load_cache()
        if cached is not None:
            return cached

    try:
        api_key = os.getenv("POLLINATIONS_API_KEY", "")
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(MODELS_API_URL, headers=headers)
            resp.raise_for_status()
            data = resp.json()

        models = data if isinstance(data, list) else data.get("data", [])
        models = [m for m in models if isinstance(m, dict) and m.get("name")]

        _save_cache(models)
        return models
    except (httpx.HTTPError, json.JSONDecodeError) as e:
        logger.warning("Failed to fetch models from Pollinations API: %s", e)
        cached = _load_cache()
        if cached is not None:
            return cached
        return []


def to_model_configs(
    models: list[dict[str, Any]], provider_name: str = "pollinations"
) -> list[ModelConfig]:
    """Convert Pollinations /text/models data to ModelConfig objects."""
    configs = []
    for m in models:
        name = m.get("name", "")
        if not name:
            continue
        description = m.get("description", "")
        pricing = m.get("pricing", {})
        input_price = pricing.get("promptTextTokens", 0.0) * 1_000_000
        output_price = pricing.get("completionTextTokens", 0.0) * 1_000_000
        context_length = m.get("context_window") or 0
        configs.append(
            ModelConfig(
                name=name,
                provider=provider_name,
                alias=name,
                description=description,
                input_price=input_price,
                output_price=output_price,
                context_length=int(context_length),
            )
        )
    return configs
