import pandas as pd

from const import (COLOR_MAP, COLUMNS_TO_KEEP, GENDER_MAP, PROCESSED_CSV_PATH,
                   RAW_CSV_PATH, TYPE_MAP)


def preprocess_data() -> pd.DataFrame:
    """Load, clean, and save processed data from the CSV.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    print(f"Loading data from: {RAW_CSV_PATH}")
    df = pd.read_csv(RAW_CSV_PATH)

    # Filter columns to keep
    df = df[COLUMNS_TO_KEEP].copy()

    # Map categorical values
    df["Type"] = df["Type"].map(TYPE_MAP).fillna("Unknown")
    df["Gender"] = df["Gender"].map(GENDER_MAP).fillna("Unknown")
    df["Color1"] = df["Color1"].map(lambda x: COLOR_MAP.get(x, "Unknown"))

    # Clean text fields
    text_cols = ["Name", "Breed1", "Description"]
    for col in text_cols:
        df[col] = df[col].fillna("Unknown").astype(str).str.strip()

    # Normalize numeric fields
    numeric_cols = ["Age", "PhotoAmt"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    # Validate duplicates and PetID
    if df["PetID"].duplicated().any():
        print("Duplicates found in PetID. They will be removed.")
        df = df.drop_duplicates(subset="PetID")

    # Save cleaned file
    PROCESSED_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_CSV_PATH, index=False)
    print(f"Processed data saved to: {PROCESSED_CSV_PATH}")

    return df
