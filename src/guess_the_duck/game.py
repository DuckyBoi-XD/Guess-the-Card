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


def _load_game_impl() -> ModuleType:
    """Load the actual game implementation.

    In an installed wheel, the game code is shipped as a normal package at
    `guess_the_duck_legacy/game.py`.

    In a development checkout, the original source lives at
    `src/GuessTheDuck.DuckyBoi_XD/game.py`.
    """

    here = pathlib.Path(__file__).resolve()

    # 1) Preferred: bundled runtime package.
    bundled = here.parent / "legacy" / "game.py"
    if bundled.is_file():
        legacy_path = bundled
    else:
        # 2) Dev fallback: repository layout.
        legacy_path = here.parents[1] / "GuessTheDuck.DuckyBoi_XD" / "game.py"

    spec = importlib.util.spec_from_file_location("guess_the_duck._legacy_game", legacy_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load game module from {legacy_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_legacy = _load_game_impl()
main = _legacy.main
