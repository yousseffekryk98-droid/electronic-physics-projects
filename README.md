# Electronic Physics Projects — Fall 2025

This repository contains the full **50-project** Electronic Physics Projects (Fall 2025) set, organized as **one project per Git branch**.

## Start here
Open [`PROJECTS.md`](PROJECTS.md) for the complete branch index grouped by instructor.

Each project branch includes:
- project objective and underlying physics/engineering concepts
- complete bill of materials (BOM)
- pin-by-pin wiring in both the README and `wiring.csv`
- starter firmware/software under `src/`
- assembly procedure and acceptance tests
- calibration/measurement guidance
- safety notes appropriate to the project
- parametric OpenSCAD mechanical/CAD source under `cad/design.scad`
- relevant open-source library/tool links where applicable

## Branch groups
- `amir-01-...` through `amir-20-...` — Dr/Amir Elmslmany
- `mostafa-01-...` through `mostafa-15-...` — Dr/Mostafa Elhoshy
- `ahmed-01-...` through `ahmed-15-...` — Dr/Ahmed Ayoub

The repository also keeps the branch generator under `.github/scripts/` and a verification workflow under `.github/workflows/`. The workflow checks that exactly **50 project branches** exist after generation.

> These are educational prototypes. Mains electricity, batteries, medical/EEG sensing, moving mechanisms, fire-related systems, water systems, solar/battery power electronics, and accessibility devices require appropriate supervision, calibration, and safety review before real-world use.
