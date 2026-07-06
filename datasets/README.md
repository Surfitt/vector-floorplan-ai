# Datasets

Large or proprietary floor-plan data lives here and is **not** committed to git.

## Layout

| Directory   | Purpose |
|-------------|---------|
| `raw/`      | Source IFC files, annotations, or third-party exports |
| `processed/` | Normalized graph/JSON representations ready for training |
| `cache/`    | Intermediate downloads, embeddings, or solver outputs |

## Conventions (to be refined)

- Prefer **IFC** as the canonical interchange format.
- Processed artifacts should be reproducible from `raw/` via scripts in `src/`.
- Document provenance (source, license, date) in a sidecar `*.meta.json` when adding data.

## Adding data

1. Place files under the appropriate subdirectory.
2. Add a short `README.md` or `*.meta.json` describing source and license.
3. Do **not** commit files larger than 1 MB without explicit approval (pre-commit enforces this).
