# Experiment Protocol
## Brain Tumor MRI Classification

**Status**: Planning document — to be finalized before Phase 3

---

## Reproducibility

All experiments must use:
- Random seed: 42 (set via `src/utils/seed.py`)
- Fixed train/val/test splits (split indices saved to disk)
- Documented hardware and software versions
- Version-controlled configurations (`configs/config.yaml`)

## Experiment Tracking

Each experiment should log:
- Configuration used
- Training/validation metrics per epoch
- Best checkpoint path
- Final test metrics
- Timestamp and experiment name

## Naming Convention

Experiments are named as:
```
{phase}_{architecture}_{variant}_{date}
```
Example: `phase3_resnet50_baseline_20261101`

## Results Reporting

- Report mean ± std over multiple runs (where feasible)
- Report metrics on held-out test set only (not validation)
- Never tune on test set

---

*This protocol will be expanded with detailed hyperparameter search strategy in Phase 3.*
