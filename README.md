# 🎬 Movie Analytics Pipeline

**Big Data Assignment**

| | |
|---|---|
| **Names** | Nada Ibrahim Elghaweet &nbsp;&nbsp;·&nbsp;&nbsp; Mazen Ayman |
| **IDs** | 231000941 &nbsp;&nbsp;·&nbsp;&nbsp; 231000718 |

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Directory Structure](#2-directory-structure)
3. [Pipeline Architecture](#3-pipeline-architecture)
4. [Components](#4-components)
   - [ingest.py](#41-ingestpy--data-ingestion)
   - [preprocess.ipynb](#42-preprocessipynb--data-preprocessing)
   - [analytics.ipynb](#43-analyticsipynb--analytics--insights)
   - [visualize.ipynb](#44-visualizeipynb--visualization)
   - [cluster.ipynb](#45-clusteripynb--clustering-analysis)
5. [Setup & Installation](#5-setup--installation)
6. [Running the Pipeline](#6-running-the-pipeline)
7. [Outputs Reference](#7-outputs-reference)
8. [Dependencies](#8-dependencies)
9. [Notes](#9-notes)
---

## 1. Project Overview

This project builds a reproducible, containerized data science pipeline that processes a raw movies dataset through five sequential stages: **ingestion → preprocessing → analytics → visualization → clustering**. Each stage is a self-contained script or notebook, and the entire pipeline is orchestrated by a single shell script (`summary.sh`) running inside Docker.

**Key goals:**
- Clean and transform messy movie data into an analysis-ready format
- Extract meaningful insights about genres, countries, and revenue
- Produce visualizations that reveal distributions and relationships in the data
- Apply unsupervised machine learning (KMeans) to discover natural movie groupings

---

## 2. Directory Structure

```
/app/pipeline/
├── ingest.py                  # Stage 1: Data ingestion
├── preprocess.ipynb           # Stage 2: Data preprocessing
├── analytics.ipynb            # Stage 3: Insights extraction
├── visualize.ipynb            # Stage 4: Visualization
├── cluster.ipynb              # Stage 5: Clustering analysis
├── summary.sh                 # Pipeline orchestrator
├── Dockerfile                 # Container definition
├── movies_updated.csv         # Raw input dataset
│
├── data_raw.csv               # Output of Stage 1
├── data_preprocessed.csv      # Output of Stage 2
│
├── insight1.txt               # Top 3 genres by average score
├── insight2.txt               # Country with highest avg score
├── insight3.txt               # Rating with highest gross revenue
│
├── summary_histograms.png     # Score, gross, votes distributions
├── summary_scatter.png        # Score vs Votes / Score vs Gross
├── summary_pairplot.png       # Pairplot of score, votes, gross
├── summary_heatmap.png        # Correlation heatmap
│
├── clusters_A.png             # Cluster plot: Score vs Votes
├── clusters_B.png             # Cluster plot: Budget vs Gross
├── clusters_C.png             # Cluster plot: All features (5D)
├── clusters.txt               # Cluster counts and labels summary
└── README.md
```

---

## 3. Pipeline Architecture

The pipeline runs sequentially. Stages 3, 4, and 5 all consume the same preprocessed CSV independently.

```
movies_updated.csv
        |
        v
   [ ingest.py ]  ─────────────────────────► data_raw.csv
        |
        v
[ preprocess.ipynb ] ────────────────────► data_preprocessed.csv
        |
        |─────────────────┬─────────────────┐
        v                 v                 v
[ analytics.ipynb ] [ visualize.ipynb ] [ cluster.ipynb ]
        |                 |                 |
        v                 v                 v
  insight1-3.txt    summary*.png    clusters*.png + clusters.txt
```

---

## 4. Components

### 4.1 `ingest.py` — Data Ingestion

**Purpose:** Loads the raw CSV dataset, prints a summary, and saves it as `data_raw.csv`.

**What it does:**
- Accepts a dataset path as a command-line argument
- Reads the CSV using `pandas`
- Prints the dataset shape and first 5 rows for a quick sanity check
- Saves the raw data as `data_raw.csv` for downstream stages

**Usage:**
```bash
python ingest.py movies_updated.csv
```

**Output:** `data_raw.csv`

---

### 4.2 `preprocess.ipynb` — Data Preprocessing

**Purpose:** Cleans, transforms, and scales the raw data into a format suitable for analysis and machine learning.

#### Data Cleaning
- Splits the `released` column into `release_date` and `release_country`, dropping the original `released` and redundant `year` columns
- Converts `release_date` to a proper datetime type
- Fills missing values in categorical columns (`rating`, `writer`, `star`, `company`, `release_country`, `release_date`) using the **mode**
- Fills missing values in `gross` using the **median**
- Identifies and reports duplicate rows

#### Feature Transformation
- Label-encodes all categorical columns: `rating`, `genre`, `country`, `director`, `writer`, `star`, `company`, `release_country`
- Fixes the malformed `runtime,,` column (removes commas, renames to `runtime`)
- Standard-scales numerical columns: `budget`, `gross`, `score`, `votes`, `runtime`

#### Dimensionality Reduction
- Selects a relevant subset of columns for analysis
- Bins `score` into 3 quantile-based categories: `Low` (0), `Medium` (1), `High` (2) → stored as `score_bin`

**Input:** `data_raw.csv` → **Output:** `data_preprocessed.csv`

---

### 4.3 `analytics.ipynb` — Analytics & Insights

**Purpose:** Derives three key business insights from the preprocessed data and saves them as text files.

| Insight | Question | Output File |
|---------|----------|-------------|
| Insight 1 | What are the top 3 genres by average score? | `insight1.txt` |
| Insight 2 | Which country has the highest average movie score? | `insight2.txt` |
| Insight 3 | Which rating category has the highest average gross revenue? | `insight3.txt` |

**Input:** `data_preprocessed.csv` → **Output:** `insight1.txt`, `insight2.txt`, `insight3.txt`

---

### 4.4 `visualize.ipynb` — Visualization

**Purpose:** Generates plots to explore distributions, relationships, and correlations in the data.

| Plot | File | Description |
|------|------|-------------|
| Histograms | `summary_histograms.png` | Distributions of score, gross revenue, and votes |
| Scatterplots | `summary_scatter.png` | Score vs Votes and Score vs Gross |
| Pairplot | `summary_pairplot.png` | Pairwise relationships between score, votes, gross |
| Heatmap | `summary_heatmap.png` | Pearson correlation matrix for numeric features |

**Input:** `data_preprocessed.csv` → **Output:** `summary_histograms.png`, `summary_scatter.png`, `summary_pairplot.png`, `summary_heatmap.png`

---

### 4.5 `cluster.ipynb` — Clustering Analysis

**Purpose:** Applies KMeans (k=3) on three different feature subsets to reveal natural movie groupings.

| Cluster Set | Features | What It Shows |
|-------------|----------|---------------|
| Cluster A | `score`, `votes` | Quality vs popularity groupings |
| Cluster B | `budget`, `gross` | Financial performance groupings |
| Cluster C | `score`, `votes`, `gross`, `budget`, `runtime` | Holistic 5-feature groupings |

**Cluster labels:**

| Cluster | A (Score/Votes) | B (Budget/Gross) | C (All Features) |
|---------|----------------|-----------------|-----------------|
| 0 | Popular & high-rated | High budget & high gross | High across all features |
| 1 | Unpopular & low-rated | Low budget & low gross | Low across all features |
| 2 | Mixed / average | Medium performance | Average / mixed |

> **Note:** Cluster C uses 5 features but is visualized on Score vs Votes axes for 2D interpretability.

**Input:** `data_preprocessed.csv` → **Output:** `clusters_A.png`, `clusters_B.png`, `clusters_C.png`, `clusters.txt`

---

## 5. Setup & Installation

### Prerequisites
- [Docker](https://www.docker.com/) installed on your machine

### Build the Docker Image

```bash
docker build -t bigdata_pipeline .
```

This automatically installs: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `scipy`, `jupyter`

---

## 6. Running the Pipeline

### Step 1 — Start the Container

```bash
docker run -it -v /path/to/Big_Data_Assignment:/app/pipeline bigdata_pipeline bash
```

> Replace `/path/to/Big_Data_Assignment` with the absolute path to your project folder.

### Step 2 — Run the Full Pipeline

```bash
chmod +x summary.sh
./summary.sh
```

This runs all 5 stages in order and saves all outputs to `/app/pipeline/`.

---

### Viewing Notebook Outputs

**Option A — Jupyter in Browser**

```bash
jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --allow-root
```

Open the URL with token shown in your terminal and navigate to `/app/pipeline/`.

**Option B — Export to HTML**

```bash
jupyter nbconvert --to html preprocess.ipynb analytics.ipynb visualize.ipynb cluster.ipynb
```

Open the generated `.html` files directly in any browser.

---

## 7. Outputs Reference

| File | Type | Generated By | Description |
|------|------|-------------|-------------|
| `data_raw.csv` | CSV | `ingest.py` | Raw dataset copy |
| `data_preprocessed.csv` | CSV | `preprocess.ipynb` | Cleaned, encoded, scaled dataset |
| `insight1.txt` | Text | `analytics.ipynb` | Top 3 genres by average score |
| `insight2.txt` | Text | `analytics.ipynb` | Country with highest average score |
| `insight3.txt` | Text | `analytics.ipynb` | Rating with highest gross revenue |
| `summary_histograms.png` | PNG | `visualize.ipynb` | Score, gross, votes distributions |
| `summary_scatter.png` | PNG | `visualize.ipynb` | Score vs Votes & Score vs Gross |
| `summary_pairplot.png` | PNG | `visualize.ipynb` | Pairplot of score, votes, gross |
| `summary_heatmap.png` | PNG | `visualize.ipynb` | Correlation heatmap |
| `clusters_A.png` | PNG | `cluster.ipynb` | KMeans: Score vs Votes clusters |
| `clusters_B.png` | PNG | `cluster.ipynb` | KMeans: Budget vs Gross clusters |
| `clusters_C.png` | PNG | `cluster.ipynb` | KMeans: All-features clusters (5D→2D) |
| `clusters.txt` | Text | `cluster.ipynb` | Cluster sizes and labels summary |

---

## 8. Dependencies

| Package | Purpose |
|---------|---------|
| `pandas` | Data loading and manipulation |
| `numpy` | Numerical operations |
| `matplotlib` | Plot rendering |
| `seaborn` | Statistical visualizations |
| `scikit-learn` | Label encoding, scaling, KMeans |
| `scipy` | Supporting scientific computations |
| `jupyter` | Notebook execution and export |

All installed automatically via the `Dockerfile`.

---

## 9. Notes

- The pipeline is **fully reproducible** inside Docker — running `summary.sh` from a clean state regenerates all outputs deterministically.
- `set -e` in `summary.sh` means the pipeline **stops immediately** if any stage fails, preventing silent downstream errors.
- KMeans uses `random_state=42` in all clustering cells for consistent results.
- `release_date` parsing uses `errors='coerce'` — unparseable dates become `NaT` and are filled with the mode.
- Label encoding is order-dependent; the `label_encoders` dictionary is retained in the notebook for potential inverse transformation.
