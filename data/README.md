# Data Directory

This directory contains the local dataset files. **No image data is committed to GitHub.**

## Structure

```
data/
├── raw/           ← Extracted Kaggle dataset (excluded from Git)
├── processed/     ← Future: preprocessed splits (excluded from Git)
└── README.md      ← This file (tracked by Git)
```

## raw/

Contains the original extracted Kaggle dataset. This directory must never be modified directly.
Files here are the ground truth for all downstream processing.

Expected structure after extraction:
```
data/raw/
├── Training/
│   ├── glioma/       (1,400 JPEG images)
│   ├── meningioma/   (1,400 JPEG images)
│   ├── notumor/      (1,400 JPEG images)
│   └── pituitary/    (1,400 JPEG images)
└── Testing/
    ├── glioma/       (400 JPEG images)
    ├── meningioma/   (400 JPEG images)
    ├── notumor/      (400 JPEG images)
    └── pituitary/    (400 JPEG images)
```

## processed/

Will contain preprocessed data splits created during Phase 2:
- `train/` — augmented training images
- `validation/` — held-out validation split
- `test/` — standardised test images

## Dataset Setup

To set up the dataset locally, extract the Kaggle ZIP into `data/raw/`:
```bash
python3 -c "import zipfile; zipfile.ZipFile('archive.zip').extractall('data/raw/')"
```
