# Project Overview
## Brain Tumor MRI Classification

**Project Type**: University Deep Learning Research Project  
**Current Phase**: Phase 1 — Dataset Analysis & GitHub Setup ✅  
**Last Updated**: October 2026  

---

## Project Goal

To develop and evaluate an end-to-end deep-learning pipeline for automated brain tumor classification from MRI images. The project addresses not only accuracy but also:
- **Explainability** — making predictions interpretable to clinicians
- **Uncertainty Estimation** — quantifying prediction confidence
- **Confidence Calibration** — ensuring predicted probabilities are reliable

---

## Complete Project Pipeline

```
Raw Dataset (7,200 MRI images, 4 classes)
          │
          ▼  Phase 1 ✅
    Dataset Validation & Analysis
    ─────────────────────────────
    • File integrity checks
    • Class distribution analysis
    • Image dimension survey
    • Duplicate / leakage checks
    • Dataset documentation
          │
          ▼  Phase 2 🔜 Planned
    Data Preprocessing & Augmentation
    ──────────────────────────────────
    • Resize to 224×224
    • Grayscale → RGB conversion
    • ImageNet normalization
    • Validation split (stratified, 15%)
    • Training augmentation
          │
          ▼  Phase 3 🔜 Planned
    Baseline Models (Transfer Learning)
    ────────────────────────────────────
    • VGG16 fine-tuned
    • ResNet50 fine-tuned
    • EfficientNetB3 fine-tuned
    • Evaluation: accuracy, F1, AUC-ROC
    • Confusion matrices
          │
          ▼  Phase 4 🔜 Planned
    Proposed Dual-Branch Architecture
    ──────────────────────────────────
    • EfficientNetB3 branch
    • ResNet50 branch
    • Feature fusion (concatenation)
    • Classification head
          │
          ▼  Phase 5 🔜 Planned
    CBAM Attention Integration
    ────────────────────────────
    • Channel attention module
    • Spatial attention module
    • Integration into dual-branch model
          │
          ▼  Phase 6 🔜 Planned
    Training Pipeline
    ──────────────────
    • Training loop with callbacks
    • Early stopping
    • Learning rate scheduling
    • Experiment tracking
          │
          ▼  Phase 7 🔜 Planned
    Evaluation & Baseline Comparison
    ─────────────────────────────────
    • Accuracy, Precision, Recall, F1
    • AUC-ROC per class
    • Confusion matrix
    • Comparison vs VGG16, ResNet50, EfficientNetB3
          │
          ▼  Phase 8 🔜 Planned
    Uncertainty Estimation
    ───────────────────────
    • Monte Carlo Dropout (N forward passes)
    • Predictive entropy
    • Mutual information
    • Uncertainty-accuracy correlation
          │
          ▼  Phase 9 🔜 Planned
    Confidence Calibration
    ───────────────────────
    • Pre-calibration reliability diagram
    • Temperature scaling (learned scalar T)
    • ECE (Expected Calibration Error)
    • Post-calibration reliability diagram
          │
          ▼  Phase 10 🔜 Planned
    Explainability
    ───────────────
    • Grad-CAM: gradient-weighted class activation maps
    • SHAP: GradientExplainer attribution maps
    • Quantitative agreement: IoU & Pearson correlation
    • Visual comparison: SHAP vs Grad-CAM
          │
          ▼  Phase 11 🔜 Planned
    Ablation Studies
    ─────────────────
    • Single-branch vs dual-branch
    • With vs without CBAM
    • With vs without augmentation
    • Architecture contribution analysis
          │
          ▼  Phase 12 🔜 Planned
    Final Analysis & Report
    ────────────────────────
    • Comprehensive results summary
    • Figures and tables
    • Final academic report
```

---

## Research Problems Addressed

| Problem | Description | Phase | Status |
|---------|-------------|-------|--------|
| Problem 1 | SHAP GradientExplainer + Grad-CAM explainability | Phase 10 | 🔜 Planned |
| Problem 2 | Monte Carlo Dropout uncertainty estimation | Phase 8 | 🔜 Planned |
| Problem 3 | Temperature scaling confidence calibration | Phase 9 | 🔜 Planned |
| Problem 4 | EfficientNetB3 + ResNet50 dual-branch fusion | Phase 4 | 🔜 Planned |
| Problem 5 | CBAM channel and spatial attention | Phase 5 | 🔜 Planned |
| Problem 6 | Ablation studies on architectural variants | Phase 11 | 🔜 Planned |
| Problem 7 | Baseline comparisons (VGG16, ResNet50, EfficientNetB3) | Phase 3 | 🔜 Planned |
| Problem 8 | Quantitative agreement: IoU + Pearson (SHAP vs Grad-CAM) | Phase 10 | 🔜 Planned |

---

## Technology Stack (Planned)

| Component | Technology |
|-----------|-----------|
| Language | Python 3.14+ |
| Deep Learning | PyTorch (planned) |
| Data Handling | NumPy, Pandas |
| Image Processing | Pillow, OpenCV |
| Visualization | Matplotlib, Seaborn |
| Explainability | SHAP, pytorch-grad-cam |
| Experiment Tracking | Weights & Biases (planned) |
| Notebooks | Jupyter |

---

## Directory Purpose Summary

| Directory | Purpose | Status |
|-----------|---------|--------|
| `data/raw/` | Original extracted dataset (read-only) | ✅ Populated |
| `data/processed/` | Future preprocessed splits | 🔜 Empty |
| `configs/` | Centralised configuration | ✅ Created |
| `notebooks/` | Phase-by-phase analysis notebooks | Phase 1 ✅ |
| `src/data/` | Dataset loading & analysis modules | Phase 1 ✅ |
| `src/preprocessing/` | Image preprocessing pipeline | 🔜 Planned |
| `src/models/` | All neural network architectures | 🔜 Planned |
| `src/training/` | Training loop & callbacks | 🔜 Planned |
| `src/evaluation/` | Metrics & evaluation utilities | 🔜 Planned |
| `src/uncertainty/` | Monte Carlo Dropout | 🔜 Planned |
| `src/calibration/` | Temperature scaling | 🔜 Planned |
| `src/explainability/` | SHAP + Grad-CAM | 🔜 Planned |
| `experiments/` | Experiment results & configs | 🔜 Planned |
| `outputs/` | Generated figures, metrics, predictions | Phase 1 ✅ (figures) |
| `reports/` | Human-readable academic reports | Phase 1 ✅ |
| `docs/` | Technical documentation | Phase 1 ✅ |
| `tests/` | Automated unit tests | 🔜 Planned |
| `app/` | Inference/demo application | 🔜 Planned |
