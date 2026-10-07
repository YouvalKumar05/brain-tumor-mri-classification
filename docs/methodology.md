# Methodology
## Brain Tumor MRI Classification

**Status**: Planning document — implementation begins Phase 2

---

## Planned Methodology

This document outlines the intended methodology for each phase of the project. It will be updated as phases are implemented and experimental choices are finalized.

### 1. Dataset

- **Source**: Kaggle Brain Tumor MRI Dataset (Nickparvar, 2021)
- **Split**: Pre-defined Training (5,600) / Testing (1,600)
- **Validation**: Stratified 15% split from training data (~840 images)

### 2. Preprocessing (Planned — Phase 2)

- Resize all images to 224×224 pixels
- Convert grayscale images to 3-channel RGB
- Normalize using ImageNet mean and standard deviation
- Training augmentation: rotation (±15°), horizontal flip, zoom (10%), brightness jitter

### 3. Baseline Models (Planned — Phase 3)

Fine-tune three standard pretrained architectures:
- VGG16 (ImageNet pretrained, final layers replaced)
- ResNet50 (ImageNet pretrained, final layers replaced)
- EfficientNetB3 (ImageNet pretrained, final layers replaced)

### 4. Proposed Architecture (Planned — Phase 4 & 5)

A dual-backbone model combining:
- **Branch 1**: EfficientNetB3 feature extractor
- **Branch 2**: ResNet50 feature extractor
- **Fusion**: Concatenation of pooled feature maps
- **Attention**: CBAM applied to fused features
- **Head**: Fully connected classification layers

### 5. Training Protocol (Planned — Phase 6)

- Optimizer: Adam (lr=1e-4, initial)
- Loss: Cross-entropy
- Batch size: 32
- Epochs: up to 50 with early stopping (patience=10)
- LR scheduling: ReduceLROnPlateau (patience=5, factor=0.5)

### 6. Evaluation (Planned — Phase 7)

- Primary: Accuracy, Macro F1-Score
- Secondary: Per-class Precision, Recall, AUC-ROC
- Confusion matrix
- Statistical comparison against baselines

### 7. Uncertainty Estimation (Planned — Phase 8)

- Monte Carlo Dropout: keep dropout active at inference time
- N=50 stochastic forward passes per image
- Metrics: predictive entropy, mutual information

### 8. Calibration (Planned — Phase 9)

- Calibration measure: Expected Calibration Error (ECE)
- Method: Temperature scaling (single scalar T, learned on validation set)
- Visualization: Reliability diagrams before/after calibration

### 9. Explainability (Planned — Phase 10)

- **Grad-CAM**: Gradient-weighted class activation maps from last conv layer
- **SHAP**: GradientExplainer with random background samples
- **Quantitative Agreement**: IoU (binary mask overlap) + Pearson correlation between normalized heatmaps

### 10. Ablation Studies (Planned — Phase 11)

Systematic ablation of:
- Dual-branch vs single-branch
- With CBAM vs without CBAM
- With augmentation vs without augmentation

---

*This document will be updated with actual experimental decisions as the project progresses.*
