"""
src/utils/visualization.py
============================
Shared visualisation utilities.

STATUS: Partial — Phase 1 (basic style helpers only)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PALETTE = {
    'glioma':     '#E74C3C',
    'meningioma': '#3498DB',
    'notumor':    '#2ECC71',
    'pituitary':  '#9B59B6',
}

def apply_style():
    """Apply consistent project-wide matplotlib style."""
    plt.rcParams.update({
        'font.family':       'DejaVu Sans',
        'axes.titlesize':    13,
        'axes.labelsize':    11,
        'figure.dpi':        150,
        'savefig.dpi':       200,
        'savefig.bbox':      'tight',
        'axes.spines.top':   False,
        'axes.spines.right': False,
    })
