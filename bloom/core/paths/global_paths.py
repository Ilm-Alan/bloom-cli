from __future__ import annotations

from collections.abc import Callable
import os
from pathlib import Path

from bloom import BLOOM_ROOT


class GlobalPath:
    def __init__(self, resolver: Callable[[], Path]) -> None:
        self._resolver = resolver

    @property
    def path(self) -> Path:
        return self._resolver()


_DEFAULT_BLOOM_HOME = Path.home() / ".bloom"


def _get_bloom_home() -> Path:
    if bloom_home := os.getenv("BLOOM_HOME"):
        return Path(bloom_home).expanduser().resolve()
    return _DEFAULT_BLOOM_HOME


BLOOM_HOME = GlobalPath(_get_bloom_home)
GLOBAL_CONFIG_FILE = GlobalPath(lambda: BLOOM_HOME.path / "config.toml")
GLOBAL_ENV_FILE = GlobalPath(lambda: BLOOM_HOME.path / ".env")
GLOBAL_TOOLS_DIR = GlobalPath(lambda: BLOOM_HOME.path / "tools")
GLOBAL_SKILLS_DIR = GlobalPath(lambda: BLOOM_HOME.path / "skills")
GLOBAL_AGENTS_DIR = GlobalPath(lambda: BLOOM_HOME.path / "agents")
GLOBAL_PROMPTS_DIR = GlobalPath(lambda: BLOOM_HOME.path / "prompts")
SESSION_LOG_DIR = GlobalPath(lambda: BLOOM_HOME.path / "logs" / "session")
TRUSTED_FOLDERS_FILE = GlobalPath(lambda: BLOOM_HOME.path / "trusted_folders.toml")
LOG_DIR = GlobalPath(lambda: BLOOM_HOME.path / "logs")
LOG_FILE = GlobalPath(lambda: BLOOM_HOME.path / "bloom.log")

DEFAULT_TOOL_DIR = GlobalPath(lambda: BLOOM_ROOT / "core" / "tools" / "builtins")
