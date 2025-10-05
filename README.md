# Pet Adoption Search

Repository for indexing and visual search of pets. It contains ETL pipelines to process the Kaggle data, scripts to load documents into Elasticsearch, and a Streamlit interface for text search and visual exploration of images.

## Contents

This README covers:

- Full project structure
- How to prepare the data (Kaggle)
- How to install dependencies with `uv sync` (and an alternative with venv)
- How to bring up Elasticsearch and Kibana with Docker Compose
- How to run the ETL pipeline and load the data
- How to run the Streamlit UI

---

## Project structure

```
Pet-Adoption-Search/
├── .gitignore
├── .python-version
├── const.py
├── docker-compose.yml
├── main.py
├── pyproject.toml
├── README.md
├── uv.lock
├── data/
│   ├── raw/
│   │   └── pet_description/      # Downloaded CSVs (train.csv,...)
│   └── processed/
│       ├── pets_json/            # Per-pet JSONs for indexing
│       └── processed_csv/        # Processed CSV
├── static/
│   └── images/                   # Images (eg. 0008c5398-1.jpg)
└── src/
	├── etl/
	│   ├── __init__.py
	│   ├── preprocess.py         # Clean/normalize CSV -> processed
	│   └── create_json_docs.py   # Generate per-pet JSONs
	├── index/
	│   ├── __init__.py
	│   └── elastic_loader.py     # Create index and load docs to ES
	└── ui/
		└── streamlit_app.py     # Streamlit app (visual search)
```

## Data (Kaggle)

Original data comes from the Kaggle competition: https://www.kaggle.com/competitions/petfinder-adoption-prediction/data

Steps to prepare the data:

1. Download files from Kaggle (e.g. `train.csv`) and put `train.csv` in `data/raw/pet_description/`.
2. Download images (e.g. `train_images`) and copy the content into `static/images/`. Images should follow the pattern `{pet_id}-1.jpg`, `{pet_id}-2.jpg`, etc., as provided by the dataset.

> Note: Large files are not versioned (`.gitignore`) to avoid uploading data to the repository.

## Install dependencies with `uv sync`

If you use the `uv` tool to manage virtual environments and dependencies:

1. Install `uv` if you don't have it:

```bash
pip install uv
```

2. From the project root run:

```bash
uv sync
```

This will create (or update) the virtual environment and sync dependencies defined in `pyproject.toml` and `uv.lock`.

3. Activate the environment if it's not activated automatically:

```bash
source .venv/bin/activate
```

4. Check that required packages are installed:

```bash
pip list
```

## Bring up Elasticsearch and Kibana (Docker Compose)

The included `docker-compose.yml` brings up Elasticsearch 8.15.3 and Kibana 8.15.3.

```bash
docker-compose up -d
```

- Elasticsearch: http://localhost:9200
- Kibana: http://localhost:5601

Verify Elasticsearch is reachable with:

```bash
curl http://localhost:9200
```

## ETL pipeline and loading into Elasticsearch

- IMPORTANT: You do NOT need to run processing, JSON generation or load steps individually. The project provides `main.py` which runs the whole pipeline in a single flow (pipe). If you prefer or need to run steps individually you can, but it's not required.

1. (Optional) If running steps individually, process CSV and generate processed JSONs:

```bash
python src/etl/preprocess.py
python src/etl/create_json_docs.py
```

2. (Optional) Load JSONs into Elasticsearch:

```bash
python src/index/elastic_loader.py
```

3. Recommended: Run the entire pipeline using `main.py` which chains the steps.

```bash
python main.py
```

4. Verify in Kibana that the index exists and inspect documents.

## Run the Streamlit app

1. Make sure you run from the project root (where `const.py` lives) and have the environment activated.
2. Run:

```bash
streamlit run src/ui/streamlit_app.py
```

The app will be available at `http://localhost:8501`.

## Performance and caching notes

- `@st.cache_resource` is used to keep the Elasticsearch connection across reruns.
- `@st.cache_data` is used to cache image reads and avoid repeated base64 encodings.

## Recommended `.gitignore` configuration

We recommend ignoring:

- `.DS_Store`
- `.python-version` (if you use pyenv locally)
- `data/` (or at least large files like `.csv`, `.json`)
- `static/images/` (if you don't want to upload images)

Example used in this repo:

```
.venv
__pycache__/
data/**/*.csv
data/**/*.json
static/images/*
.DS_Store
.python-version
```

## Development and contributions

- To develop, create a feature branch, add tests and open a PR.
- Keep the README updated if you change scripts or module names.

## Contact

Felipe Alvarez Zuloaga

felipealvarezzuloaga@gmail.com
