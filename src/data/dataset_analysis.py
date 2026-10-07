"""
Brain Tumor MRI Classification
================================
src/data/dataset_analysis.py

Phase 1 — Dataset Analysis
----------------------------
Performs comprehensive analysis of the Brain Tumor MRI dataset.
All statistics are calculated from the actual downloaded files.
No values are fabricated or assumed.

Classes
-------
    DatasetAnalyzer : Main analysis class

Usage
-----
    python3 src/data/dataset_analysis.py

    Or import and use:
        from src.data.dataset_analysis import DatasetAnalyzer
        analyzer = DatasetAnalyzer('data/raw')
        results = analyzer.run_full_analysis()
"""

import os
import sys
import hashlib
import warnings
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Optional, Tuple

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for script mode
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from PIL import Image
import seaborn as sns

# ── Suppress non-critical warnings ──────────────────────────────────────────
warnings.filterwarnings('ignore', category=UserWarning)

# ── Project root detection ───────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).resolve().parent          # src/data/
PROJECT_ROOT = SCRIPT_DIR.parent.parent                 # project root
RAW_DATA_DIR = PROJECT_ROOT / 'data' / 'raw'
OUTPUT_DIR   = PROJECT_ROOT / 'outputs' / 'figures' / 'dataset'

# ── Constants ────────────────────────────────────────────────────────────────
SPLITS  = ['Training', 'Testing']
CLASSES = ['glioma', 'meningioma', 'notumor', 'pituitary']

CLASS_DISPLAY = {
    'glioma':     'Glioma',
    'meningioma': 'Meningioma',
    'notumor':    'No Tumor',
    'pituitary':  'Pituitary',
}

# Colour palette (per class, consistent across all charts)
CLASS_COLORS = {
    'glioma':     '#E74C3C',
    'meningioma': '#3498DB',
    'notumor':    '#2ECC71',
    'pituitary':  '#9B59B6',
}

# ── Style ────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family':       'DejaVu Sans',
    'axes.titlesize':    13,
    'axes.labelsize':    11,
    'xtick.labelsize':   10,
    'ytick.labelsize':   10,
    'legend.fontsize':   10,
    'figure.dpi':        150,
    'savefig.dpi':       200,
    'savefig.bbox':      'tight',
    'axes.spines.top':   False,
    'axes.spines.right': False,
})


# ════════════════════════════════════════════════════════════════════════════
class DatasetAnalyzer:
    """
    Comprehensive analyser for the Brain Tumor MRI dataset.

    Parameters
    ----------
    raw_data_dir : str | Path
        Path to the extracted raw dataset root (contains Training/ and Testing/).
    output_dir : str | Path
        Directory where generated figures are saved.
    """

    def __init__(
        self,
        raw_data_dir: Optional[Path] = None,
        output_dir:   Optional[Path] = None,
    ):
        self.raw_data_dir = Path(raw_data_dir) if raw_data_dir else RAW_DATA_DIR
        self.output_dir   = Path(output_dir)   if output_dir   else OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Analysis results stored here after run_full_analysis()
        self.results: Dict = {}

    # ── 1. Count images ─────────────────────────────────────────────────────
    def count_images(self) -> Dict:
        """Return per-split, per-class image counts."""
        print("  [1/9] Counting images per split and class …")
        counts = {}
        for split in SPLITS:
            counts[split] = {}
            split_dir = self.raw_data_dir / split
            if not split_dir.exists():
                print(f"        WARNING: {split_dir} does not exist.")
                continue
            for cls in CLASSES:
                cls_dir = split_dir / cls
                if not cls_dir.exists():
                    counts[split][cls] = 0
                    continue
                images = [
                    f for f in cls_dir.iterdir()
                    if f.is_file() and f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
                ]
                counts[split][cls] = len(images)
        return counts

    # ── 2. File extensions ───────────────────────────────────────────────────
    def scan_extensions(self) -> Dict[str, int]:
        """Count all file extensions present in the dataset."""
        print("  [2/9] Scanning file extensions …")
        ext_counter: Counter = Counter()
        for split in SPLITS:
            for cls in CLASSES:
                cls_dir = self.raw_data_dir / split / cls
                if not cls_dir.exists():
                    continue
                for f in cls_dir.iterdir():
                    if f.is_file():
                        ext_counter[f.suffix.lower() or '(no extension)'] += 1
        return dict(ext_counter.most_common())

    # ── 3. Image dimension survey ────────────────────────────────────────────
    def survey_dimensions(self, sample_size: int = 200) -> Dict:
        """
        Sample images across the dataset and collect dimension statistics.
        Reads at most `sample_size` images to keep runtime reasonable.
        """
        print(f"  [3/9] Surveying image dimensions (sampling up to {sample_size} images) …")
        widths, heights, channels_list, modes = [], [], [], []
        all_paths: List[Path] = []

        for split in SPLITS:
            for cls in CLASSES:
                cls_dir = self.raw_data_dir / split / cls
                if not cls_dir.exists():
                    continue
                paths = sorted(cls_dir.glob('*.jpg')) + sorted(cls_dir.glob('*.jpeg'))
                all_paths.extend(paths)

        # Random sample without replacement
        rng = np.random.default_rng(42)
        sample_paths = rng.choice(
            all_paths,
            size=min(sample_size, len(all_paths)),
            replace=False,
        ).tolist()

        corrupt, empty = 0, 0
        for p in sample_paths:
            if p.stat().st_size == 0:
                empty += 1
                continue
            try:
                with Image.open(p) as img:
                    w, h   = img.size
                    mode   = img.mode
                    n_ch   = len(img.getbands())
                    widths.append(w)
                    heights.append(h)
                    channels_list.append(n_ch)
                    modes.append(mode)
            except Exception:
                corrupt += 1

        dim_counter = Counter(zip(widths, heights))
        most_common_dims = dim_counter.most_common(5)

        mode_counter = Counter(modes)

        return {
            'widths':           widths,
            'heights':          heights,
            'channels':         channels_list,
            'modes':            dict(mode_counter),
            'min_width':        int(min(widths))  if widths  else None,
            'max_width':        int(max(widths))  if widths  else None,
            'min_height':       int(min(heights)) if heights else None,
            'max_height':       int(max(heights)) if heights else None,
            'mean_width':       float(np.mean(widths))  if widths  else None,
            'mean_height':      float(np.mean(heights)) if heights else None,
            'most_common_dims': most_common_dims,
            'sample_size':      len(sample_paths),
            'corrupt_in_sample': corrupt,
            'empty_in_sample':  empty,
        }

    # ── 4. Corrupt / unreadable image scan ──────────────────────────────────
    def scan_corrupt_images(self, max_scan: int = 500) -> Dict:
        """
        Scan up to max_scan images across the full dataset for corruption.
        Returns counts of corrupt, empty and unexpected files.
        """
        print(f"  [4/9] Scanning for corrupt / unreadable images (up to {max_scan}) …")
        corrupt, empty, unexpected = 0, 0, 0
        scanned = 0
        corrupt_list: List[str] = []

        for split in SPLITS:
            for cls in CLASSES:
                cls_dir = self.raw_data_dir / split / cls
                if not cls_dir.exists():
                    continue
                for f in sorted(cls_dir.iterdir()):
                    if scanned >= max_scan:
                        break
                    if not f.is_file():
                        continue
                    if f.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}:
                        unexpected += 1
                        continue
                    if f.stat().st_size == 0:
                        empty += 1
                        scanned += 1
                        continue
                    try:
                        with Image.open(f) as img:
                            img.verify()
                        scanned += 1
                    except Exception as e:
                        corrupt += 1
                        corrupt_list.append(f"{split}/{cls}/{f.name}: {e}")
                        scanned += 1

        return {
            'scanned':        scanned,
            'corrupt':        corrupt,
            'empty':          empty,
            'unexpected':     unexpected,
            'corrupt_files':  corrupt_list[:20],   # store first 20
        }

    # ── 5. Duplicate filename check ──────────────────────────────────────────
    def check_duplicate_filenames(self) -> Dict:
        """
        Check for duplicate filenames within and across classes/splits.
        Note: filename duplicates across classes are expected (naming convention).
        """
        print("  [5/9] Checking for duplicate filenames …")
        all_names: List[str] = []
        for split in SPLITS:
            for cls in CLASSES:
                cls_dir = self.raw_data_dir / split / cls
                if not cls_dir.exists():
                    continue
                for f in cls_dir.iterdir():
                    if f.is_file():
                        all_names.append(f.name)

        name_counter = Counter(all_names)
        duplicates = {k: v for k, v in name_counter.items() if v > 1}

        return {
            'total_filenames':       len(all_names),
            'unique_filenames':      len(name_counter),
            'duplicate_filenames':   len(duplicates),
            'examples':              list(duplicates.items())[:10],
        }

    # ── 6. Duplicate image hash check (subset) ───────────────────────────────
    def check_duplicate_images(self, sample_size: int = 600) -> Dict:
        """
        Hash-based duplicate image detection on a random subset.
        Full dataset hashing would be very slow; this is a statistical check.
        """
        print(f"  [6/9] Checking for duplicate images via MD5 hash (sample={sample_size}) …")
        all_paths: List[Path] = []
        for split in SPLITS:
            for cls in CLASSES:
                cls_dir = self.raw_data_dir / split / cls
                if not cls_dir.exists():
                    continue
                all_paths.extend(sorted(cls_dir.glob('*.jpg')))

        rng = np.random.default_rng(42)
        sample = rng.choice(
            all_paths,
            size=min(sample_size, len(all_paths)),
            replace=False,
        ).tolist()

        hash_map: Dict[str, List[str]] = defaultdict(list)
        for p in sample:
            try:
                md5 = hashlib.md5(p.read_bytes()).hexdigest()
                hash_map[md5].append(str(p.relative_to(self.raw_data_dir)))
            except Exception:
                pass

        duplicates = {k: v for k, v in hash_map.items() if len(v) > 1}

        return {
            'sampled':          len(sample),
            'unique_hashes':    len(hash_map),
            'duplicate_groups': len(duplicates),
            'examples':         list(duplicates.items())[:5],
        }

    # ── 7. Train/test overlap check (subset) ─────────────────────────────────
    def check_train_test_overlap(self, sample_size: int = 300) -> Dict:
        """
        Check for image-level train/test leakage by hashing a random subset
        from each split and comparing.
        """
        print(f"  [7/9] Checking for train/test image overlap (sample={sample_size} per split) …")

        def get_hashes(split: str, n: int) -> set:
            all_p: List[Path] = []
            for cls in CLASSES:
                cls_dir = self.raw_data_dir / split / cls
                if cls_dir.exists():
                    all_p.extend(sorted(cls_dir.glob('*.jpg')))
            rng = np.random.default_rng(42)
            sample = rng.choice(
                all_p,
                size=min(n, len(all_p)),
                replace=False,
            ).tolist()
            hashes = set()
            for p in sample:
                try:
                    hashes.add(hashlib.md5(Path(p).read_bytes()).hexdigest())
                except Exception:
                    pass
            return hashes

        train_hashes = get_hashes('Training', sample_size)
        test_hashes  = get_hashes('Testing',  sample_size)
        overlap      = train_hashes & test_hashes

        return {
            'train_sampled': len(train_hashes),
            'test_sampled':  len(test_hashes),
            'overlap_found': len(overlap),
        }

    # ── 8. Class balance analysis ────────────────────────────────────────────
    def compute_class_balance(self, counts: Dict) -> Dict:
        """Compute class balance ratios from count dictionary."""
        print("  [8/9] Computing class balance …")
        balance = {}
        for split in SPLITS:
            if split not in counts:
                continue
            split_total = sum(counts[split].values())
            balance[split] = {
                cls: {
                    'count':   counts[split][cls],
                    'percent': round(100 * counts[split][cls] / split_total, 2)
                    if split_total > 0 else 0.0,
                }
                for cls in CLASSES
            }
        return balance

    # ── 9. Generate figures ──────────────────────────────────────────────────
    def generate_figures(self, counts: Dict, dim_info: Dict) -> List[str]:
        """Generate and save all dataset visualisation figures."""
        print("  [9/9] Generating visualisation figures …")
        saved = []

        saved += self._fig_class_distribution(counts)
        saved += self._fig_sample_grid()
        saved += self._fig_dimension_distribution(dim_info)
        saved += self._fig_combined_distribution(counts)

        return saved

    # ── Figure helpers ────────────────────────────────────────────────────────
    def _fig_class_distribution(self, counts: Dict) -> List[str]:
        """Bar charts for training and testing class distribution."""
        fig, axes = plt.subplots(1, 2, figsize=(13, 5))
        fig.suptitle('Class Distribution — Brain Tumor MRI Dataset',
                     fontsize=15, fontweight='bold', y=1.02)

        for ax, split in zip(axes, SPLITS):
            cls_names  = [CLASS_DISPLAY[c] for c in CLASSES]
            cls_counts = [counts.get(split, {}).get(c, 0) for c in CLASSES]
            colors     = [CLASS_COLORS[c] for c in CLASSES]

            bars = ax.bar(cls_names, cls_counts, color=colors,
                          edgecolor='white', linewidth=0.8, width=0.6)
            for bar, cnt in zip(bars, cls_counts):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 10,
                    str(cnt),
                    ha='center', va='bottom', fontsize=10, fontweight='bold',
                )
            ax.set_title(f'{split} Set', fontsize=13, fontweight='bold')
            ax.set_xlabel('Tumor Class')
            ax.set_ylabel('Number of Images')
            ax.set_ylim(0, max(cls_counts) * 1.18)
            ax.tick_params(axis='x', rotation=15)
            for spine in ['top', 'right']:
                ax.spines[spine].set_visible(False)

        plt.tight_layout()
        path = self.output_dir / 'class_distribution.png'
        fig.savefig(path)
        plt.close(fig)
        print(f"        Saved: {path}")
        return [str(path)]

    def _fig_combined_distribution(self, counts: Dict) -> List[str]:
        """Grouped bar chart — Training vs Testing per class."""
        fig, ax = plt.subplots(figsize=(10, 6))

        x        = np.arange(len(CLASSES))
        width    = 0.35
        tr_vals  = [counts.get('Training', {}).get(c, 0) for c in CLASSES]
        te_vals  = [counts.get('Testing',  {}).get(c, 0) for c in CLASSES]
        cls_lbls = [CLASS_DISPLAY[c] for c in CLASSES]

        b1 = ax.bar(x - width / 2, tr_vals, width, label='Training',
                    color=[CLASS_COLORS[c] for c in CLASSES],
                    alpha=0.85, edgecolor='white')
        b2 = ax.bar(x + width / 2, te_vals, width, label='Testing',
                    color=[CLASS_COLORS[c] for c in CLASSES],
                    alpha=0.45, edgecolor='white', hatch='//')

        for bar, cnt in zip(list(b1) + list(b2), tr_vals + te_vals):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 10,
                str(cnt),
                ha='center', va='bottom', fontsize=9, fontweight='bold',
            )

        ax.set_title('Training vs Testing Class Distribution',
                     fontsize=14, fontweight='bold')
        ax.set_xlabel('Tumor Class', fontsize=11)
        ax.set_ylabel('Number of Images', fontsize=11)
        ax.set_xticks(x)
        ax.set_xticklabels(cls_lbls)
        ax.set_ylim(0, max(tr_vals) * 1.20)

        # Custom legend
        patch_train = mpatches.Patch(color='grey', alpha=0.85,  label='Training')
        patch_test  = mpatches.Patch(color='grey', alpha=0.45, hatch='//', label='Testing')
        ax.legend(handles=[patch_train, patch_test], fontsize=10)

        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)

        plt.tight_layout()
        path = self.output_dir / 'combined_class_distribution.png'
        fig.savefig(path)
        plt.close(fig)
        print(f"        Saved: {path}")
        return [str(path)]

    def _fig_sample_grid(self) -> List[str]:
        """4×4 grid of sample MRI images (one per class × 4 samples)."""
        fig = plt.figure(figsize=(14, 14))
        fig.suptitle('Sample Brain MRI Images — All Four Classes',
                     fontsize=16, fontweight='bold', y=0.98)

        gs = gridspec.GridSpec(4, 4, figure=fig, hspace=0.35, wspace=0.1)

        for row_idx, cls in enumerate(CLASSES):
            cls_dir = self.raw_data_dir / 'Training' / cls
            if not cls_dir.exists():
                continue
            img_paths = sorted(cls_dir.glob('*.jpg'))[:4]

            for col_idx, img_path in enumerate(img_paths):
                ax = fig.add_subplot(gs[row_idx, col_idx])
                try:
                    with Image.open(img_path) as img:
                        ax.imshow(img, cmap='gray' if img.mode == 'L' else None)
                    ax.axis('off')
                    if col_idx == 0:
                        ax.set_title(
                            CLASS_DISPLAY[cls],
                            fontsize=12, fontweight='bold',
                            color=CLASS_COLORS[cls],
                            loc='left',
                        )
                except Exception:
                    ax.axis('off')
                    ax.text(0.5, 0.5, 'Error', ha='center', va='center',
                            transform=ax.transAxes)

        path = self.output_dir / 'sample_mri_grid.png'
        fig.savefig(path, bbox_inches='tight')
        plt.close(fig)
        print(f"        Saved: {path}")
        return [str(path)]

    def _fig_dimension_distribution(self, dim_info: Dict) -> List[str]:
        """Scatter plot of image width vs height from the sample."""
        widths  = dim_info.get('widths', [])
        heights = dim_info.get('heights', [])
        if not widths:
            return []

        fig, axes = plt.subplots(1, 2, figsize=(13, 5))
        fig.suptitle('Image Dimension Distribution (sampled)',
                     fontsize=14, fontweight='bold')

        # Scatter
        ax = axes[0]
        ax.scatter(widths, heights, alpha=0.35, color='#3498DB', s=20, edgecolors='none')
        ax.set_xlabel('Width (px)')
        ax.set_ylabel('Height (px)')
        ax.set_title('Width vs Height')
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)

        # Histogram of widths
        ax2 = axes[1]
        ax2.hist(widths, bins=30, color='#E74C3C', alpha=0.75, edgecolor='white')
        ax2.set_xlabel('Width (px)')
        ax2.set_ylabel('Count')
        ax2.set_title('Width Distribution')
        for spine in ['top', 'right']:
            ax2.spines[spine].set_visible(False)

        plt.tight_layout()
        path = self.output_dir / 'dimension_distribution.png'
        fig.savefig(path)
        plt.close(fig)
        print(f"        Saved: {path}")
        return [str(path)]

    # ── Full analysis pipeline ───────────────────────────────────────────────
    def run_full_analysis(self) -> Dict:
        """
        Execute the complete dataset analysis pipeline.

        Returns
        -------
        dict : All analysis results.
        """
        print("\n" + "═" * 60)
        print("  Brain Tumor MRI Dataset Analysis")
        print("═" * 60)
        print(f"  Dataset root : {self.raw_data_dir}")
        print(f"  Output dir   : {self.output_dir}")
        print("─" * 60)

        counts    = self.count_images()
        exts      = self.scan_extensions()
        dim_info  = self.survey_dimensions()
        corrupt   = self.scan_corrupt_images()
        dup_names = self.check_duplicate_filenames()
        dup_imgs  = self.check_duplicate_images()
        overlap   = self.check_train_test_overlap()
        balance   = self.compute_class_balance(counts)
        figures   = self.generate_figures(counts, dim_info)

        # ── Summary totals ────────────────────────────────────────────────
        total_train = sum(counts.get('Training', {}).values())
        total_test  = sum(counts.get('Testing',  {}).values())
        total_all   = total_train + total_test

        self.results = {
            'counts':         counts,
            'extensions':     exts,
            'dimensions':     dim_info,
            'corrupt':        corrupt,
            'dup_filenames':  dup_names,
            'dup_images':     dup_imgs,
            'train_test_overlap': overlap,
            'class_balance':  balance,
            'total_train':    total_train,
            'total_test':     total_test,
            'total_all':      total_all,
            'figures':        figures,
        }

        self._print_summary()
        return self.results

    # ── Console summary ──────────────────────────────────────────────────────
    def _print_summary(self):
        r  = self.results
        ct = r['counts']
        b  = r['class_balance']
        d  = r['dimensions']
        co = r['corrupt']
        ov = r['train_test_overlap']
        di = r['dup_images']

        print("\n" + "═" * 60)
        print("  ANALYSIS RESULTS")
        print("═" * 60)

        print(f"\n  Total images   : {r['total_all']:>6}")
        print(f"  Training       : {r['total_train']:>6}")
        print(f"  Testing        : {r['total_test']:>6}")
        print(f"  Classes        : {len(CLASSES):>6}")

        print("\n  Per-Class Counts:")
        print(f"  {'Class':<14} {'Train':>8} {'Test':>8} {'Total':>8}  {'Balance':>8}")
        print("  " + "-" * 52)
        for cls in CLASSES:
            tr  = ct.get('Training', {}).get(cls, 0)
            te  = ct.get('Testing',  {}).get(cls, 0)
            tot = tr + te
            pct = round(100 * tr / r['total_train'], 1) if r['total_train'] else 0
            print(f"  {CLASS_DISPLAY[cls]:<14} {tr:>8} {te:>8} {tot:>8}  {pct:>6.1f}%")

        print(f"\n  Extensions found: {r['extensions']}")

        if d['min_width'] is not None:
            print(f"\n  Image Dimensions (from {d['sample_size']}-image sample):")
            print(f"    Width  : {d['min_width']}–{d['max_width']} px"
                  f"  (mean {d['mean_width']:.0f} px)")
            print(f"    Height : {d['min_height']}–{d['max_height']} px"
                  f"  (mean {d['mean_height']:.0f} px)")
            print(f"    Modes  : {d['modes']}")
            print(f"    Top dimensions : {d['most_common_dims'][:3]}")

        print(f"\n  Quality Checks (scanned {co['scanned']} images):")
        print(f"    Corrupt          : {co['corrupt']}")
        print(f"    Empty files      : {co['empty']}")
        print(f"    Unexpected files : {co['unexpected']}")

        print(f"\n  Duplicate Filename Check:")
        print(f"    Duplicate filenames across all paths : {r['dup_filenames']['duplicate_filenames']}")

        print(f"\n  Duplicate Image (Hash) Check — {di['sampled']}-image sample:")
        print(f"    Duplicate image groups found : {di['duplicate_groups']}")

        print(f"\n  Train/Test Leakage Check (MD5 hash, subset):")
        print(f"    Train sample : {ov['train_sampled']} images")
        print(f"    Test  sample : {ov['test_sampled']}  images")
        print(f"    Overlapping  : {ov['overlap_found']} images")

        print(f"\n  Figures saved to: {self.output_dir}")
        print("═" * 60 + "\n")


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == '__main__':
    # Allow overriding path via command-line argument
    data_root = Path(sys.argv[1]) if len(sys.argv) > 1 else RAW_DATA_DIR

    if not data_root.exists():
        print(f"\n  ERROR: Dataset not found at '{data_root}'")
        print("  Please extract the dataset first:")
        print("    python3 -c \"import zipfile; zipfile.ZipFile('archive.zip').extractall('data/raw/')\"")
        sys.exit(1)

    analyzer = DatasetAnalyzer(raw_data_dir=data_root)
    analyzer.run_full_analysis()
