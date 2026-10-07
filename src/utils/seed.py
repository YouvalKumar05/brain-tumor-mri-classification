"""
src/utils/seed.py
==================
Reproducibility utilities — set global random seeds.
"""
import random
import numpy as np

def set_seed(seed: int = 42) -> None:
    """Set random seeds for Python, NumPy, and (when available) PyTorch/TF."""
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark     = False
    except ImportError:
        pass
    try:
        import tensorflow as tf
        tf.random.set_seed(seed)
    except ImportError:
        pass
