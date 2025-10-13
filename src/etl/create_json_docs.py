import json

import pandas as pd

from const import PROCESSED_CSV_PATH, PROCESSED_JSON_DIR

from src.index.embeddings import get_embedding


def create_json_documents() -> int:
    """Convert the processed CSV into individual JSON documents for Elasticsearch.

    Returns:
        int: The total number of JSON documents created.
    """

    print(f"Loading processed data from: {PROCESSED_CSV_PATH}")
    df = pd.read_csv(PROCESSED_CSV_PATH)

    # Create directory if it doesn't exist
    PROCESSED_JSON_DIR.mkdir(parents=True, exist_ok=True)

    for _, row in df.iterrows():
        doc = {
            "pet_id": row["PetID"],
            "type": row["Type"],
            "name": row["Name"],
            "age": int(row["Age"]),
            "breed": row["Breed1"],
            "gender": row["Gender"],
            "color": row["Color1"],
            "description": row["Description"],
            "photo_amount": int(row["PhotoAmt"]),
            "embedding": get_embedding(row["Description"]),
        }

        # Save each document as a JSON file
        json_path = PROCESSED_JSON_DIR / f"{row['PetID']}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=4)

    print(f"{len(df)} JSON documents created in: {PROCESSED_JSON_DIR}")

    return len(df)
