# This file contains the actual CLI entry point for the PyPI distribution
# `guess-the-duck`.
#
# The project previously stored its code in a directory named
# `src/GuessTheDuck.DuckyBoi_XD/` (note the dot in the directory name), which is
# not an importable Python package. That caused wheels to be built without the
# game code, and console scripts like `guess-the-duck`/`GTD` failed at runtime.
#
# Keeping the gameplay code unchanged, we import it from the legacy location.

from __future__ import annotations

import importlib.util
import pathlib
import sys
from types import ModuleType


def _load_legacy_module() -> ModuleType:
    legacy_path = pathlib.Path(__file__).resolve().parents[1] / "GuessTheDuck.DuckyBoi_XD" / "game.py"

    spec = importlib.util.spec_from_file_location("guess_the_duck._legacy_game", legacy_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load legacy game module from {legacy_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_legacy = _load_legacy_module()
main = _legacy.main
