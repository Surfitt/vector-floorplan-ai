# vector-floorplan-ai
A generative AI framework for open-BIM architectural floor plans derived from natural language constraints.

## 🚀 Overview
Archigen is an open-source project designed to bridge the gap between human language and professional Building Information Modeling (BIM). Instead of producing static raster images, this system generates structured, IFC-based (Industry Foundation Classes) spatial models directly from text-based architectural requirements (the "Program of Requirements").

By leveraging advanced AI techniques, we translate semantic input into geometric and relational data, ready for immediate integration into professional CAD/BIM workflows.

## 🏗️ The Problem
Architectural firms spend significant time manually drafting and validating floor plans that must comply with complex requirements (square footage, circulation, lighting, and zoning). Current generative AI tools prioritize visual pixel output, which is functionally useless for construction documentation. The industry requires semantically rich, editable vector data.

## 🛠️ Technical Architecture & Methodology
This project adopts an "AI-first, BIM-compliant" approach:

- Generative Core: Utilization of [e.g., Graph Neural Networks / Transformer-based spatial sampling] to generate spatial configurations that adhere to architectural logic.

- Constraint Satisfaction: Integration of a solver-engine to validate compliance with building codes, circulation efficiency, and room connectivity.

- IFC Interoperability: Native generation of IFC data, ensuring seamless compatibility with major BIM software including Vectorworks, Revit, and Archicad.

- Synthetic Data: Utilizing diffusion models to create large-scale datasets of valid architectural floor plans for model training.

## ⚙️ Key Features
- Text-to-Space Parsing: Translating written requirements into a spatial graph representation.

- IFC Export Pipeline: Automatic generation of IFC files maintaining spatial hierarchy and object metadata (e.g., room types, area calculations).

- Constraint-Aware Generation: AI models trained to respect fundamental architectural rules and spatial relationships.

## 🚧 Roadmap
[ ] Define the JSON schema for mapping text requirements to spatial constraints.

[ ] Develop the graph-based layout generator prototype.

[ ] Implement the IFC export pipeline using ifcopenshell.

[ ] Build optimization loops for iterative constraint validation.

## 🤝 Contribution
This project is currently in the research and development phase. Contributions and discussions regarding Generative AI, BIM standards, and architectural automation are highly encouraged. Please feel free to open an issue to start a discussion.

## 🧰 Development setup

```bash
# Option A: conda (recommended)
conda env create -f environment.yml
conda activate vector-floorplan-ai

# Option B: venv + pip
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install

# Common tasks
make test    # run unit tests
make lint    # ruff check + format check
```

### Logging

Every script should call `setup_logging()` once at startup. Logs go to stderr and `logs/vector-floorplan-ai.log` (rotating, 10 MB / 7 days).

```python
from vector_floorplan_ai.logging import logger, setup_logging

setup_logging()
logger.info("Pipeline started")
```

Configure via `.env` or environment variables: `LOG_LEVEL` (TRACE–CRITICAL), `LOG_DIR`, `LOG_FILE`, `LOG_TO_CONSOLE`, `LOG_TO_FILE`.

See `AGENTS.md` for project state, architecture notes, and agent-oriented context.

## 📄 License
