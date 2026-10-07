# 🧠 Brain Tumor MRI Classification

> End-to-end brain tumor MRI classification with dataset analysis, deep learning, dual-branch architecture, uncertainty estimation, confidence calibration, and explainability.

---

## 📌 Project Overview

This project develops and evaluates a deep-learning pipeline for classifying brain MRI scans into four categories:

| Class | Description |
|-------|-------------|
| Glioma | Malignant brain tumors arising from glial cells |
| Meningioma | Tumors arising from meninges (often benign) |
| Pituitary | Tumors located in the pituitary gland |
| No Tumor | Healthy brain scans with no detectable tumor |

The project addresses not only classification accuracy but also **model explainability**, **uncertainty estimation**, and **confidence calibration** — critical properties for clinical decision support systems.

---

## 🎯 Problem Statement

Medical AI systems often operate as black boxes, providing predictions without insight into *why* a decision was made or *how confident* the model truly is. This project investigates:

- **Problem 1**: Black-box predictions — SHAP GradientExplainer and Grad-CAM visualizations
- **Problem 2**: Uncertainty estimation — Monte Carlo Dropout with multiple forward passes
- **Problem 3**: Confidence calibration — Temperature scaling and reliability diagrams
- **Problem 4**: Dual-backbone feature fusion — EfficientNetB3 + ResNet50 dual-branch architecture
- **Problem 5**: Attention mechanisms — CBAM channel and spatial attention
- **Problem 6**: Ablation studies — Comparing architectural variants
- **Problem 7**: Baseline comparisons — VGG16, ResNet50, EfficientNetB3
- **Problem 8**: Quantitative explainability agreement — IoU and Pearson correlation between SHAP and Grad-CAM

---

## 📁 Dataset

- **Source**: [Brain Tumor MRI Dataset](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset) — Kaggle
- **Total Images**: 7,200
- **Classes**: 4 (Glioma, Meningioma, Pituitary, No Tumor)
- **Training Set**: 5,600 images (1,400 per class)
- **Testing Set**: 1,600 images (400 per class)
- **Format**: JPEG, RGB
- **Split**: Perfectly balanced across all classes

> ⚠️ The dataset is **not** stored in this repository. See [Dataset Setup](#dataset-setup) below.

---

## 🗂️ Repository Structure

```
Brain_Major_Project/
│
├── data/                          # Dataset (excluded from Git — local only)
│   ├── raw/                       # Extracted Kaggle dataset (original, unmodified)
│   ├── processed/                 # Future: preprocessed/augmented splits
│   └── README.md
│
├── configs/
│   └── config.yaml                # Central project configuration
│
├── notebooks/
│   ├── 01_dataset_analysis.ipynb  # ✅ Phase 1: Dataset EDA (current)
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_baseline_models.ipynb
│   ├── 04_dual_branch_model.ipynb
│   ├── 05_uncertainty_calibration.ipynb
│   ├── 06_explainability.ipynb
│   └── 07_ablation_study.ipynb
│
├── src/                           # Source code (all reusable modules)
│   ├── data/                      # Dataset loading and splitting
│   ├── preprocessing/             # Image preprocessing and augmentation
│   ├── models/                    # All neural network architectures
│   │   ├── baselines/             # VGG16, ResNet50, EfficientNetB3
│   │   ├── attention/             # CBAM attention
│   │   └── proposed/              # Dual-branch fusion model
│   ├── training/                  # Training loop and callbacks
│   ├── evaluation/                # Metrics and evaluation utilities
│   ├── uncertainty/               # Monte Carlo Dropout
│   ├── calibration/               # Temperature scaling
│   ├── explainability/            # SHAP, Grad-CAM, agreement metrics
│   ├── experiments/               # Experiment orchestration
│   └── utils/                     # Shared utilities
│
├── experiments/                   # Experiment results and configs
├── outputs/                       # Generated figures, metrics, predictions
├── reports/                       # Human-readable academic reports
│   └── dataset_analysis/          # ✅ Phase 1 report (current)
├── docs/                          # Project documentation
├── screenshots/                   # GitHub workflow screenshots
├── tests/                         # Automated tests
└── app/                           # Future inference/demo application
```

---

## 📊 Current Status

| Phase | Description | Status |
|-------|-------------|--------|
| **Phase 1** | Dataset Analysis & GitHub Setup | ✅ **Completed** |
| Phase 2 | Data Preprocessing & Augmentation | 🔜 Planned |
| Phase 3 | Baseline Models (VGG16, ResNet50, EfficientNetB3) | 🔜 Planned |
| Phase 4 | Dual-Branch Architecture (EfficientNetB3 + ResNet50) | 🔜 Planned |
| Phase 5 | CBAM Attention Module | 🔜 Planned |
| Phase 6 | Training Pipeline | 🔜 Planned |
| Phase 7 | Evaluation & Metrics | 🔜 Planned |
| Phase 8 | Monte Carlo Dropout / Uncertainty | 🔜 Planned |
| Phase 9 | Temperature Scaling / Calibration | 🔜 Planned |
| Phase 10 | SHAP + Grad-CAM Explainability | 🔜 Planned |
| Phase 11 | Ablation Studies | 🔜 Planned |
| Phase 12 | Final Analysis & Report | 🔜 Planned |

---

## ⚙️ Dataset Setup

The dataset is **not** stored in this GitHub repository (images are excluded via `.gitignore`).

**To set up the dataset locally:**

1. Download the dataset from Kaggle:
   - [Brain Tumor MRI Dataset](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset)
2. Place the `archive.zip` in the project root.
3. Extract it into `data/raw/`:
   ```bash
   python3 -c "import zipfile; zipfile.ZipFile('archive.zip').extractall('data/raw/')"
   ```
4. Verify the structure:
   ```
   data/raw/
   ├── Training/
   │   ├── glioma/       (1400 images)
   │   ├── meningioma/   (1400 images)
   │   ├── notumor/      (1400 images)
   │   └── pituitary/    (1400 images)
   └── Testing/
       ├── glioma/       (400 images)
       ├── meningioma/   (400 images)
       ├── notumor/      (400 images)
       └── pituitary/    (400 images)
   ```

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/brain-tumor-mri-classification.git
cd brain-tumor-mri-classification

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Set up dataset (see Dataset Setup above)
```

---

## 📈 Dataset Analysis

The Phase 1 dataset analysis is available in:

- **Notebook**: [`notebooks/01_dataset_analysis.ipynb`](notebooks/01_dataset_analysis.ipynb)
- **Script**: [`src/data/dataset_analysis.py`](src/data/dataset_analysis.py)
- **Report**: [`reports/dataset_analysis/brain_tumor_dataset_analysis.pdf`](reports/dataset_analysis/brain_tumor_dataset_analysis.pdf)
- **Figures**: [`outputs/figures/dataset/`](outputs/figures/dataset/)
- **Documentation**: [`docs/dataset_observations.md`](docs/dataset_observations.md)

To run the analysis:
```bash
python3 src/data/dataset_analysis.py
```

---

## 🔬 Future Development

The following components are **planned** for future implementation phases:

- **Preprocessing pipeline**: Resizing, normalization, augmentation strategies
- **Baseline models**: Transfer learning with VGG16, ResNet50, EfficientNetB3
- **Dual-branch model**: Parallel EfficientNetB3 + ResNet50 with feature fusion
- **CBAM attention**: Channel and spatial attention mechanisms
- **Monte Carlo Dropout**: Bayesian-style uncertainty estimation
- **Temperature scaling**: Post-hoc confidence calibration
- **Grad-CAM**: Gradient-weighted class activation maps
- **SHAP**: SHapley Additive exPlanations using GradientExplainer
- **Quantitative agreement**: IoU and Pearson correlation between attribution methods
- **Ablation studies**: Systematic analysis of architectural contributions
- **Web application**: Inference demo application

---

## 📄 License

MIT License — see [`LICENSE`](LICENSE) for details.

---

## 🔗 References

- Nickparvar, M. (2021). Brain Tumor MRI Dataset. Kaggle.
- Selvaraju, R. R., et al. (2017). Grad-CAM: Visual explanations from deep networks via gradient-based localization.
- Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions (SHAP).
- Gal, Y., & Ghahramani, Z. (2016). Dropout as a Bayesian approximation.
- Woo, S., et al. (2018). CBAM: Convolutional Block Attention Module.
