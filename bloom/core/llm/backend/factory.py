from __future__ import annotations

from bloom.core.config import Backend
from bloom.core.llm.backend.generic import GenericBackend

BACKEND_FACTORY = {Backend.GENERIC: GenericBackend}
