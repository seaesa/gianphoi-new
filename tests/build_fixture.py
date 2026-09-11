"""Chạy build đúng một lần cho cả bộ test."""
from __future__ import annotations

import functools
import os

from scripts.build import ROOT, build


@functools.lru_cache(maxsize=1)
def ensure_built() -> tuple[str, ...]:
    return tuple(build(ROOT))


def read_output(relpath: str) -> str:
    ensure_built()
    with open(os.path.join(ROOT, relpath), encoding="utf-8") as handle:
        return handle.read()
