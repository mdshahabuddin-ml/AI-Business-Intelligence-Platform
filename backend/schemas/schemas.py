from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DatasetOut(BaseModel):
    id: int
    filename: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class CleaningReport(BaseModel):
    dataset_id: int
    rows_before: int
    rows_after: int
    duplicates_removed: int
    missing_values_filled: dict
    columns_type_fixed: dict
    outliers_flagged: dict