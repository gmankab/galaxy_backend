# ruff: noqa: F401
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.resolve()))
import core.main

app = core.main.app

