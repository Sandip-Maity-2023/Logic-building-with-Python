import re

import pandas as pd


REQUIRED_COLUMNS = [
    "name",
    "online_order",
    "book_table",
    "rate",
    "votes",
    "approx_cost(for two people)",
    "listed_in(type)",
]


def parse_rating(value):
    if pd.isna(value):
        return 0.0
    match = re.search(r"\d+(\.\d+)?", str(value))
    return float(match.group(0)) if match else 0.0


def parse_number(value):
    if pd.isna(value):
        return 0
    cleaned = re.sub(r"[^0-9.]", "", str(value))
    return int(float(cleaned)) if cleaned else 0


def normalize_yes_no(value):
    value = str(value).strip().title()
    return "Yes" if value == "Yes" else "No"


def load_restaurant_data(filepath):
    df = pd.read_csv(filepath)

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing)}")

    df = df[REQUIRED_COLUMNS].copy()
    df["name"] = df["name"].fillna("Unknown Restaurant").astype(str).str.strip()
    df["online_order"] = df["online_order"].apply(normalize_yes_no)
    df["book_table"] = df["book_table"].apply(normalize_yes_no)
    df["rate"] = df["rate"].apply(parse_rating)
    df["votes"] = df["votes"].apply(parse_number)
    df["approx_cost(for two people)"] = df["approx_cost(for two people)"].apply(parse_number)
    df["listed_in(type)"] = df["listed_in(type)"].fillna("Other").astype(str).str.strip()
    df = df[df["name"].ne("")]
    return df.reset_index(drop=True)


def preprocess_data(filepath):
    df = load_restaurant_data(filepath)
    df.to_csv(filepath, index=False)
    return df
