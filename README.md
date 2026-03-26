
#  Movie Analytics Pipeline

**Big Data Assignment**
 Names : Nada Ibrahim Elghaweet       ,      Mazen Ayman
 IDs :   231000941                    ,     231000718

---

## Table of Contents

1. [Project Overview]
2. [Directory Structure]
3. [Pipeline Architecture]
4. [Components]
   - [ingest.py]
   - [preprocess.ipynb]
   - [analytics.ipynb]
   - [visualize.ipynb]
   - [cluster.ipynb]
5. [Setup & Installation]
6. [Running the Pipeline]
7. [Outputs Reference]
8. [Dependencies]
9. [Notes]

---

## 1. Project Overview

This project builds a reproducible, containerized data science pipeline that processes a raw movies dataset through five sequential stages: **ingestion → preprocessing → analytics → visualization → clustering**. Each stage is a self-contained script or notebook, and the entire pipeline is orchestrated by a single shell script (`summary.sh`) and runs inside Docker for full reproducibility.

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
│
└── README.md
```

---

## 3. Pipeline Architecture

```
movies_updated.csv
       │
       ▼
┌─────────────────┐
│   ingest.py     │  → data_raw.csv
└─────────────────┘
       │
       ▼
┌─────────────────────┐
│  preprocess.ipynb   │  → data_preprocessed.csv
└─────────────────────┘
       │
       ├──────────────────────────────────────────┐──────────────────────────────────────────────┐
       ▼                                          ▼                                              ▼
┌─────────────────┐                   ┌─────────────────────┐                         ┌─────────────────────┐
│ analytics.ipynb │ → insight1-3.txt  │  visualize.ipynb    │ → summary*.png          │    cluster.ipynb    │
└─────────────────┘                   └─────────────────────┘                         └─────────────────────┘
                                                                                                 │
                                                                                                 ▼
                                                                                     clusters*.png, clusters.txt
               
               
```

The pipeline is executed sequentially by `summary.sh`. Each stage depends on the CSV output of the previous (ingest.py or preprocessed.ipynb) stage.

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

**Steps performed:**

**Data Cleaning**
- Splits the `released` column into `release_date` and `release_country`, dropping the original `released` and redundant `year` columns
- Converts `release_date` to a proper datetime type
- Fills missing values in categorical columns (`rating`, `writer`, `star`, `company`, `release_country`, `release_date`) using the **mode**
- Fills missing values in `gross` using the **median**
- Identifies and reports duplicate rows

**Feature Transformation**
- Label-encodes all categorical columns: `rating`, `genre`, `country`, `director`, `writer`, `star`, `company`, `release_country`
- Fixes the malformed `runtime,,` column (removes commas, renames to `runtime`)
- Standard-scales numerical columns: `budget`, `gross`, `score`, `votes`, `runtime`

**Dimensionality Reduction**
- Selects a relevant subset of columns for analysis
- Bins `score` into 3 quantile-based categories: `Low` (0), `Medium` (1), `High` (2) → stored as `score_bin`

**Input:** `data_raw.csv`
**Output:** `data_preprocessed.csv`

---

### 4.3 `analytics.ipynb` — Analytics & Insights

**Purpose:** Derives three key business insights from the preprocessed data and saves them as text files.

| Insight | Question | Output File |
|---------|----------|-------------|
| Insight 1 | What are the top 3 genres by average score? | `insight1.txt` |
| Insight 2 | Which country has the highest average movie score? | `insight2.txt` |
| Insight 3 | Which rating category has the highest average gross revenue? | `insight3.txt` |

Each insight is printed to the console and saved to its corresponding `.txt` file.

**Input:** `data_preprocessed.csv`
**Output:** `insight1.txt`, `insight2.txt`, `insight3.txt`

---

### 4.4 `visualize.ipynb` — Visualization

**Purpose:** Generates a set of publication-quality plots to explore distributions, relationships, and correlations in the data.

**Plots produced:**

**Histograms** (`summary_histograms.png`)
- Distribution of movie scores — reveals how scores are concentrated
- Distribution of gross revenue — shows the revenue skew across movies
- Distribution of votes — shows popularity spread

**Scatterplots** (`summary_scatter.png`)
- Score vs Votes — explores the relationship between popularity and quality
- Score vs Gross — explores whether high-grossing movies tend to score better

**Pairplot** (`summary_pairplot.png`)
- Full pairwise relationships between `score`, `votes`, and `gross`

**Correlation Heatmap** (`summary_heatmap.png`)
- Numeric correlation matrix for `score`, `votes`, `gross`, `budget`, `runtime`
- Annotated with Pearson correlation coefficients

**Input:** `data_preprocessed.csv`
**Output:** `summary_histograms.png`, `summary_scatter.png`, `summary_pairplot.png`, `summary_heatmap.png`

---

### 4.5 `cluster.ipynb` — Clustering Analysis

**Purpose:** Applies KMeans clustering (k=3) on three different feature subsets to reveal natural groupings of movies.

| Cluster | Features Used | Interpretation |
|---------|--------------|----------------|
| Cluster A | `score`, `votes` | Groups movies by quality and popularity |
| Cluster B | `budget`, `gross` | Groups movies by financial profile |
| Cluster C | `score`, `votes`, `gross`, `budget`, `runtime` | Holistic grouping across all key features |

**Cluster A labels:**
- Cluster 0 → Popular & high-rated
- Cluster 1 → Unpopular & low-rated
- Cluster 2 → Mixed / average

**Cluster B labels:**
- Cluster 0 → High budget & high gross
- Cluster 1 → Low budget & low gross
- Cluster 2 → Medium performance

**Cluster C labels:**
- Cluster 0 → High across all features
- Cluster 1 → Low across all features
- Cluster 2 → Average / mixed

> **Note:** Cluster C uses 5 features. The plot visualizes it in 2D (Score vs Votes axes) for interpretability.

Each clustering run saves a scatter plot and a summary of cluster sizes to `clusters.txt`.

**Input:** `data_preprocessed.csv`
**Output:** `clusters_A.png`, `clusters_B.png`, `clusters_C.png`, `clusters.txt`

---

## 5. Setup & Installation

### Prerequisites
- [Docker](https://www.docker.com/) installed on your machine

### Build the Docker Image

```bash
docker build -t bigdata_pipeline .
```

This installs all required Python packages automatically:
- `pandas`, `numpy`, `matplotlib`, `seaborn`
- `scikit-learn`, `scipy`
- `jupyter`

---

## 6. Running the Pipeline

### Step 1 — Start the Container

```bash
docker run -it -v /path/to/Big_Data_Assignment:/app/pipeline bigdata_pipeline bash
```

> Replace `/path/to/Big_Data_Assignment` with the absolute path to your project folder on your machine.

### Step 2 — Run the Full Pipeline

Inside the container:

```bash
chmod +x summary.sh
./summary.sh
```

This executes all 5 stages sequentially:
1. `python ingest.py movies_updated.csv`
2. `jupyter nbconvert --execute preprocess.ipynb`
3. `jupyter nbconvert --execute analytics.ipynb`
4. `jupyter nbconvert --execute visualize.ipynb`
5. `jupyter nbconvert --execute cluster.ipynb`

All outputs are saved to `/app/pipeline/`.

---

### Viewing Notebook Outputs

**Option A — Jupyter in Browser**

```bash
jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --allow-root
```

Open the URL with token shown in your terminal. Navigate to `/app/pipeline/` to view notebooks interactively.

**Option B — Export to HTML**

```bash
jupyter nbconvert --to html preprocess.ipynb
jupyter nbconvert --to html analytics.ipynb
jupyter nbconvert --to html visualize.ipynb
jupyter nbconvert --to html cluster.ipynb
```

Open the generated `.html` files directly in any browser — no Jupyter needed.

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

All dependencies are installed automatically via the `Dockerfile`.

| Package | Version | Purpose |
|---------|---------|---------|
| `pandas` | latest | Data loading, manipulation |
| `numpy` | latest | Numerical operations |
| `matplotlib` | latest | Plot rendering |
| `seaborn` | latest | Statistical visualizations |
| `scikit-learn` | latest | Label encoding, scaling, KMeans |
| `scipy` | latest | Supporting scientific computations |
| `jupyter` | latest | Notebook execution and export |

---

## 9. Notes

- The pipeline is **fully reproducible** inside Docker. Running `summary.sh` from a clean state will regenerate all outputs deterministically.
- `set -e` in `summary.sh` means the pipeline will **stop immediately** if any stage fails, preventing silent downstream errors.
- KMeans results may vary slightly between runs unless `random_state=42` is honored — it is set in all clustering cells.
- The `release_date` parsing uses `errors='coerce'`, so any unparseable dates become `NaT` and are filled with the mode.
- Label encoding is order-dependent; the `label_encoders` dictionary is retained in the notebook for potential inverse transformation.
=======
# big-data-movie-pipeline

 
 
