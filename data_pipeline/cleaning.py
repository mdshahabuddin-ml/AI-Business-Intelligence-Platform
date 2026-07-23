import pandas as pd
import numpy as np


def remove_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    return df, removed


def fix_column_types(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    fixed = {}
    for col in df.columns:
        if df[col].dtype == object:
            coerced_numeric = pd.to_numeric(df[col], errors="coerce")
            non_null_ratio = coerced_numeric.notna().mean()
            if non_null_ratio > 0.8:
                df[col] = coerced_numeric
                fixed[col] = "numeric"
                continue

            coerced_date = pd.to_datetime(df[col], errors="coerce")
            non_null_ratio_date = coerced_date.notna().mean()
            if non_null_ratio_date > 0.8:
                df[col] = coerced_date
                fixed[col] = "datetime"
    return df, fixed


def fill_missing_values(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    filled = {}
    for col in df.columns:
        missing_count = int(df[col].isna().sum())
        if missing_count == 0:
            continue

        if pd.api.types.is_numeric_dtype(df[col]):
            fill_value = df[col].median()
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            fill_value = df[col].mode().iloc[0] if not df[col].mode().empty else pd.NaT
        else:
            fill_value = df[col].mode().iloc[0] if not df[col].mode().empty else "Unknown"

        df[col] = df[col].fillna(fill_value)
        filled[col] = missing_count
    return df, filled


def flag_outliers(df: pd.DataFrame) -> dict:
    outlier_counts = {}
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        count = int(((df[col] < lower) | (df[col] > upper)).sum())
        if count > 0:
            outlier_counts[col] = count
    return outlier_counts


def clean_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    rows_before = len(df)

    df, duplicates_removed = remove_duplicates(df)
    df, types_fixed = fix_column_types(df)
    df, missing_filled = fill_missing_values(df)
    outliers = flag_outliers(df)

    report = {
        "rows_before": rows_before,
        "rows_after": len(df),
        "duplicates_removed": duplicates_removed,
        "columns_type_fixed": types_fixed,
        "missing_values_filled": missing_filled,
        "outliers_flagged": outliers,
    }
    return df, report


def profile_dataset(df: pd.DataFrame) -> dict:
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category", "str"]).columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime64[ns]"]).columns.tolist()

    summary = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "datetime_columns": datetime_cols,
        "numeric_summary": {},
        "categorical_summary": {},
        "correlation_matrix": {},
    }

    for col in numeric_cols:
        summary["numeric_summary"][col] = {
            "mean": float(df[col].mean()),
            "median": float(df[col].median()),
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "std": float(df[col].std()) if len(df[col]) > 1 else 0.0,
        }

    for col in categorical_cols:
        top_values = df[col].value_counts().head(5).to_dict()
        summary["categorical_summary"][col] = {str(k): int(v) for k, v in top_values.items()}

    if len(numeric_cols) > 1:
        corr = df[numeric_cols].corr().round(3)
        summary["correlation_matrix"] = corr.to_dict()

    return summary
