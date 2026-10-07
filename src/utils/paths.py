"""
src/utils/paths.py
===================
Centralised path resolution for the project.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

DATA_RAW       = PROJECT_ROOT / 'data' / 'raw'
DATA_PROCESSED = PROJECT_ROOT / 'data' / 'processed'
CONFIGS        = PROJECT_ROOT / 'configs'
NOTEBOOKS      = PROJECT_ROOT / 'notebooks'
OUTPUTS        = PROJECT_ROOT / 'outputs'
FIGURES        = OUTPUTS / 'figures'
METRICS        = OUTPUTS / 'metrics'
CHECKPOINTS    = OUTPUTS / 'checkpoints'
REPORTS        = PROJECT_ROOT / 'reports'

def get_class_dir(split: str, cls: str) -> Path:
    """Return path to a class directory in the raw dataset."""
    return DATA_RAW / split / cls
