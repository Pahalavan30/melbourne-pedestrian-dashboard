# Victoria Urban Planning - Urban Streetscape Intervention Analysis

This repository is for the SIT Capstone "Chameleon Project" in partnership with Infrastructure Victoria.

## Table of Contents
1. Project Overview
2. Business Problem & Research Question
3. Stream Structure
4. Tech Stack
5. Architecture & Key Components
6. Data Sources & CRS Warning
7. Directory Structure
8. Installation, Setup & Execution
9. Git Workflow & Collaboration Guide
10. Coding Standards

## Project Overview
Infrastructure Victoria is an independent advisory body providing evidence-based research to the Victorian Government. This project evaluates the real-world impacts of streetscape interventions (like new bike lanes, road reallocations, and pedestrian upgrades) on transport efficiency, sustainability, and livability. 

The goal is to develop a repeatable analytical framework to deliver clear, decision-ready insights for future infrastructure investments.

**Team & Roles:**
- **Product Owners:** Matthew Raisbeck & Danielle Rebbechi (Infrastructure Victoria)
- **Mentor:** Scott West

## Business Problem & Research Question
Understanding the impacts on businesses, parking utilization, and movement patterns when road space is reallocated is complex. We are leveraging public datasets to provide data-driven evidence of these impacts, accounting for challenges like COVID-19 behavioral shifts.

**Research Question:**
> How does parking use change with bike lanes constructed?

- **Null Hypothesis:** There has been no change in parking capacity or utilization.
- **Scope:** Metropolitan Melbourne and Regional Victoria, prioritizing protected bike lanes datasets.
- **Objective:** Understand how many people are using parking spaces before and after bike lane interventions, and the economic/social impacts of those changes.

## Stream Structure
The project is divided into four stakeholder-focused streams:
1. Cycling and public transport mode shift
2. Traffic volumes and parking
3. Pedestrian counts
4. Temporal patterns

**Note:** All streams must share the same foundational tech stack and methodology to avoid sprawl and ensure the final insights are cohesive.

## Tech Stack
- **Backend:** Python (FastAPI, DuckDB, pandas, geopandas, shapely, uvicorn)
- **Frontend:** React, Vite, MapLibre GL, Recharts
- **Languages:** Python, JavaScript, R (planned)
- **Visualization:** Custom React Dashboard
- **GIS Tools:** QGIS or ArcGIS
- **Notebooks:** JupyterLab (for data exploration)


## Data Sources & CRS Warning
We are using public datasets from:
- Data.vic.gov.au
- Open Data Transport Victoria (opendata.transport.vic.gov.au)
- VicRoads datasets
- Public Transport Victoria (PTV) data
- Google Maps / Street View / aerial imagery

**Important CRS Warning:**
Datasets from different sources (e.g., VicRoads vs. PTV) are unlikely to share the same spatial coordinate systems (CRS). You must define and document CRS reprojections in your notebooks/scripts. Do not assume all datasets share the same ground truth.

*Note: ABS Census data releases in August. Population data integration will be deferred until after the release to avoid mid-sprint disruption. Use proxy labeling approaches where ground truth is absent, and document proxy methods in the `src/` directory.*

## Directory Structure

Please adhere to this structure to keep the repo organized and facilitate collaboration across streams:

```
Victoria-Urban-Planning/
├── .github/            # GitHub configuration (e.g., Pull Request templates)
├── data/
│   ├── raw/            # Original, untouched datasets
│   ├── processed/      # Cleaned and transformed datasets
│   └── parking_analytics.duckdb # DuckDB database for parking analytics
├── team_a/             # Stream 1: Cycling and public transport mode shift / Stream 3: Pedestrian counts
│   ├── notebooks/      # Stream 1 & 3 research and EDA notebooks
│   └── __init__.py
├── team_b/             # Stream 2: Traffic volumes and parking
│   ├── notebooks/      # Stream 2 research and EDA notebooks
│   └── __init__.py
├── team_c/             # Stream 4: Temporal patterns
│   ├── notebooks/      # Stream 4 research and EDA notebooks
│   └── __init__.py
├── CODING_STANDARDS.md # Shared coding guidelines and best practices
├── DATA.md             # Detailed dataset inventory and proxy methodology
├── README.md           # Project documentation and setup guide
├── config.yaml         # Configuration file for data paths and sources
├── requirements.txt    # Python baseline dependencies
├── run_ingestion.py    # Pipeline orchestration runner
└── scratchpad.txt      # Temporary scratchpad for notes and queries
```

## Installation, Setup & Execution

To explore the datasets, run the data ingestion workflow, and perform exploratory data analysis (EDA), follow these steps to set up the Python environment and launch JupyterLab.

### 1. Environment Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Chameleon-company/Victoria-Urban-Planning.git
   cd Victoria-Urban-Planning
   ```

2. **Create the Python Virtual Environment:**
   ```bash
   python3 -m venv .venv
   ```

3. **Activate the Virtual Environment:**
   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```
   - **Windows:**
     ```cmd
     .venv\Scripts\activate
     ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 2. Running JupyterLab & Data Exploration

Launch JupyterLab to interact with the notebooks:
```bash
jupyter lab
```

### 3. Data Ingestion & Pipeline Orchestration

For Stream 2 (Traffic Volumes & Parking), you can run the full ingestion pipeline by navigating to the Stream 2 workspace:
1. Open the [00_data_ingestion.ipynb](team_b/notebooks/scott_z/00_data_ingestion.ipynb) notebook.
2. Run the cells sequentially to download base GeoJSON datasets, download and extract historical parking sensor CSVs, and execute the end-to-end ETL processing steps to build the DuckDB database.

## Git Workflow & Collaboration Guide

### Rules
1. Never commit directly to the `main` branch.
2. Use the Branch Naming Convention.
3. PRs with merge conflicts will not be approved or merged. You are responsible for resolving conflicts locally.

### Branch Naming Convention
Branches must use the following format:
- `feature/<your-initials>/<description>`
- `bugfix/<your-initials>/<description>`

Examples:
- `feature/sz/add-traffic-pipeline`
- `bugfix/sz/fix-crs-reprojection`

### Step-by-Step Workflow

**1. Start Fresh**
Always create your branch from the latest `main`:
```bash
git checkout main
git pull origin main
git checkout -b feature/<your-initials>/<description>
```

**2. Work and Commit**
Make your changes, then add and commit with a clear message:
```bash
git add .
git commit -m "Add traffic volume parsing for Metro Melbourne"
```

**3. Rebase Against `main`**
Before pushing, you must rebase on top of the latest `main` to pull in changes and resolve conflicts locally:
```bash
git fetch origin
git rebase origin/main
```
If there are merge conflicts, Git will pause. Open the files, fix the issues, and run:
```bash
git add <fixed-files>
git rebase --continue
```

**4. Push and Open a PR**
Push your branch and open a PR on GitHub:
```bash
git push -u origin <your-branch-name>
```
*(If you already pushed before rebasing, use `git push --force-with-lease origin <your-branch-name>`)*

**5. Review and Merge**
Assign reviewers from your stream. Once approved, the PR can be merged.

## Coding Standards
All contributors are expected to follow our shared coding standards covering PEP 8, Tidyverse, docstrings, and security. Please read the full [Coding Standards & Best Practices Guide](CODING_STANDARDS.md) before writing code.
