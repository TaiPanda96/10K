from pathlib import Path
import os

def get_project_root() -> Path:
    return Path(__file__).parent.parent