from src.etl.create_json_docs import create_json_documents
from src.etl.preprocess import preprocess_data
from src.index.elastic_loader import run_index_pipeline

if __name__ == "__main__":
    print("Preprocessing pipeline and JSON document creation.\n")
    df = preprocess_data()

    print("\n Creating JSON documents...")
    total_docs = create_json_documents()
    print(f"\n Pipeline complete. Total documents generated: {total_docs}")

    print("\n Starting Elasticsearch load...")
    run_index_pipeline()
    print("\n Process completed successfully.")
