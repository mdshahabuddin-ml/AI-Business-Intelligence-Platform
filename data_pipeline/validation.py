import pandas as pd

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
MAX_FILE_SIZE_MB = 50


def validate_extension(filename: str) -> bool:
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)


def load_dataframe(path: str) -> pd.DataFrame:
    if path.lower().endswith(".csv"):
        return pd.read_csv(path)
    return pd.read_excel(path)


def validate_dataframe(df: pd.DataFrame) -> list[str]:
    warnings = []
    if df.empty:
        warnings.append("Uploaded file has no rows.")
    if len(df.columns) == 0:
        warnings.append("Uploaded file has no columns.")
    if df.columns.duplicated().any():
        warnings.append("Duplicate column names detected.")
    return warnings
