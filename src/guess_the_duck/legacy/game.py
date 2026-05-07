"""Legacy game implementation.

This module provides a stable import target inside the published wheel.

We intentionally avoid importing from the original package name
`GuessTheDuck.DuckyBoi_XD` because that is not a valid Python package layout
and may not be importable when installed.

Instead, we load the legacy `game.py` implementation from a file that is
shipped inside this distribution.

NOTE: Keep `legacy_source_game.py` in sync with
`src/GuessTheDuck.DuckyBoi_XD/game.py`.
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys
from types import ModuleType


def _load() -> ModuleType:
    here = pathlib.Path(__file__).resolve()
    legacy_path = here.with_name("legacy_source_game.py")

    spec = importlib.util.spec_from_file_location("guess_the_duck._legacy_source_game", legacy_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load legacy game module from {legacy_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_impl = _load()

# Re-export the entrypoint expected by console scripts.
main = _impl.main
