"""Legacy game implementation.

This file is a vendored copy of the original game code so the installed
distribution can run without relying on repository-only paths.

NOTE: Keep this file in sync with `src/GuessTheDuck.DuckyBoi_XD/game.py`.
"""

from __future__ import annotations

# The actual game code is maintained in the original module.
# For development checkouts, importing it directly is fine.
# For installed wheels, this file provides a stable import target.

from ...GuessTheDuck.DuckyBoi_XD.game import *  # type: ignore
