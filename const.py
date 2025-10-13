from pathlib import Path

# Directory paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
PROCESSED_CSV_DIR = PROCESSED_DIR / "processed_csv"
PROCESSED_JSON_DIR = PROCESSED_DIR / "pets_json"
STATIC_DIR = BASE_DIR / "static"
IMAGE_DIR = STATIC_DIR / "images"

# File paths
RAW_CSV_PATH = RAW_DIR / "pet_description" / "train.csv"
PROCESSED_CSV_PATH = PROCESSED_CSV_DIR / "train_processed.csv"

# Mappings
TYPE_MAP = {1: "Dog", 2: "Cat"}
GENDER_MAP = {1: "Male", 2: "Female", 3: "Mixed"}
COLOR_MAP = {
    1: "Black",
    2: "Brown",
    3: "Golden",
    4: "Yellow",
    5: "Cream",
    6: "Gray",
    7: "White",
}

# Columns to keep after preprocessing
COLUMNS_TO_KEEP = [
    "PetID",
    "Type",
    "Name",
    "Age",
    "Breed1",
    "Gender",
    "Color1",
    "Description",
    "PhotoAmt",
]

# Elasticsearch configuration
INDEX_NAME = "pet_adoption_index"

INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "pet_id": {"type": "keyword"},
            "type": {"type": "keyword"},
            "name": {"type": "text"},
            "age": {"type": "integer"},
            "breed": {"type": "text"},
            "gender": {"type": "keyword"},
            "color": {"type": "keyword"},
            "description": {"type": "text"},
            "photo_amount": {"type": "integer"},
            "image_url": {"type": "keyword"},
            "embedding": {
                "type": "dense_vector",
                "dims": 384,  # depende del modelo, MiniLM tiene 384
                "index": True,
                "similarity": "cosine"
            }
        }
    }
}

# Elasticsearch host
DEFAULT_ES_HOST = "http://localhost:9200"
