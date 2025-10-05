import json
from pathlib import Path

from elasticsearch import Elasticsearch, helpers

from const import (DEFAULT_ES_HOST, INDEX_MAPPING, INDEX_NAME,
                   PROCESSED_JSON_DIR)


def connect_elasticsearch() -> Elasticsearch:
    """Create a local Elasticsearch client.

    Returns:
        Elasticsearch: The Elasticsearch client instance.
    """

    es = Elasticsearch(
        [DEFAULT_ES_HOST],
        verify_certs=False,
        ssl_show_warn=False,
    )

    try:
        if es.ping():
            print("Connected to Elasticsearch")
        else:
            raise ConnectionError
    except Exception as e:
        raise ConnectionError(f"Not able to connect to Elasticsearch: {e}")

    return es


def create_index(es):
    """Create the Elasticsearch index if it doesn't exist.

    Args:
        es (Elasticsearch): The Elasticsearch client instance.
    """
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body=INDEX_MAPPING)
        print(f"Index '{INDEX_NAME}' created.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")


def load_documents_to_es(es):
    """Load documents from JSON files into Elasticsearch.

    Args:
        es (Elasticsearch): The Elasticsearch client instance.
    """
    json_files = list(Path(PROCESSED_JSON_DIR).glob("*.json"))
    print(f"Preparing to load {len(json_files)} documents...")

    actions = []
    for fpath in json_files:
        with open(fpath, "r", encoding="utf-8") as f:
            doc = json.load(f)
            actions.append({"_index": INDEX_NAME, "_id": doc["pet_id"], "_source": doc})

    helpers.bulk(es, actions)
    print(f"{len(actions)} documents indexed in '{INDEX_NAME}'.")


def run_index_pipeline():
    """Run the full indexing pipeline: connect, create index, and load documents."""
    es = connect_elasticsearch()
    create_index(es)
    load_documents_to_es(es)
