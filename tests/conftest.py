"""
Make the package in the repo importable when the tests are run directly
from the source tree (without requiring `pip install -e .`).
"""
from __future__ import annotations
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]   # …/quantstats_lumi project root
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))
