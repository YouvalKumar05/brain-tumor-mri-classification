# App Directory

**Status**: Planned — Future Phase

This directory will contain a web-based or command-line inference application for the trained brain tumor classifier.

## Planned Contents

- `app.py` — Main application entry point
- `inference.py` — Model loading and prediction logic
- `templates/` — HTML templates (if web UI)
- `static/` — Static assets (if web UI)
- `requirements_app.txt` — App-specific dependencies

## Intended Usage (Future)

```bash
python3 app/app.py --image path/to/mri.jpg
```

Or as a web interface:
```bash
python3 app/app.py --serve --port 8080
```

Implementation will begin after the core model training and evaluation phases are complete.
