"""Unit tests for the data cleaning pipeline. Run with: python -m pytest tests/unit/ -v"""
import pandas as pd

from data_pipeline.validation import validate_extension, load_dataframe, validate_dataframe
from data_pipeline.cleaning import clean_dataset, profile_dataset


def test_validate_extension_accepts_csv():
    assert validate_extension("sales.csv") is True
    assert validate_extension("sales.xlsx") is True
    assert validate_extension("sales.txt") is False


def test_load_dataframe_reads_sample_csv():
    df = load_dataframe("storage/uploads/sample_sales.csv")
    assert len(df) == 15
    assert "Sales" in df.columns


def test_validate_dataframe_passes_on_good_data():
    df = load_dataframe("storage/uploads/sample_sales.csv")
    warnings = validate_dataframe(df)
    assert warnings == []


def test_clean_dataset_removes_duplicate():
    df = load_dataframe("storage/uploads/sample_sales.csv")
    cleaned_df, report = clean_dataset(df)
    assert report["duplicates_removed"] == 1
    assert report["rows_after"] == report["rows_before"] - 1


def test_clean_dataset_fills_missing_values():
    df = load_dataframe("storage/uploads/sample_sales.csv")
    cleaned_df, report = clean_dataset(df)
    assert cleaned_df.isna().sum().sum() == 0
    assert "Sales" in report["missing_values_filled"]
    assert "Profit" in report["missing_values_filled"]


def test_clean_dataset_flags_planted_outlier():
    df = load_dataframe("storage/uploads/sample_sales.csv")
    cleaned_df, report = clean_dataset(df)
    assert "Sales" in report["outliers_flagged"]
    assert report["outliers_flagged"]["Sales"] >= 1


def test_profile_dataset_returns_expected_structure():
    df = load_dataframe("storage/uploads/sample_sales.csv")
    cleaned_df, _ = clean_dataset(df)
    profile = profile_dataset(cleaned_df)

    assert profile["row_count"] == len(cleaned_df)
    assert "Sales" in profile["numeric_columns"]
    assert "Region" in profile["categorical_columns"]
    assert "mean" in profile["numeric_summary"]["Sales"]
