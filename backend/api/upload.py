import json
import os
import shutil
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from backend.config.settings import settings
from backend.database import get_db
from backend.schemas.schemas import DatasetOut, CleaningReport
from backend.security import get_current_user
from data_pipeline.validation import validate_extension, load_dataframe, validate_dataframe
from data_pipeline.cleaning import clean_dataset, profile_dataset
from database.models import Dataset, User

router = APIRouter(tags=["datasets"])


@router.post("/upload/dataset", response_model=DatasetOut)
def upload_dataset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not validate_extension(file.filename):
        raise HTTPException(status_code=400, detail="Only .csv, .xlsx, .xls files are supported")

    os.makedirs(settings.upload_dir, exist_ok=True)
    unique_name = f"{uuid.uuid4().hex}_{file.filename}"
    save_path = os.path.join(settings.upload_dir, unique_name)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        df = load_dataframe(save_path)
    except Exception as exc:
        os.remove(save_path)
        raise HTTPException(status_code=400, detail=f"Could not parse file: {exc}")

    warnings = validate_dataframe(df)
    if warnings:
        os.remove(save_path)
        raise HTTPException(status_code=400, detail=f"Validation failed: {'; '.join(warnings)}")

    dataset = Dataset(
        filename=file.filename,
        original_path=save_path,
        status="uploaded",
        owner_id=current_user.id,
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset


@router.post("/data/clean/{dataset_id}", response_model=CleaningReport)
def clean_dataset_endpoint(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id, Dataset.owner_id == current_user.id
    ).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    df = load_dataframe(dataset.original_path)
    cleaned_df, report = clean_dataset(df)

    os.makedirs(settings.processed_dir, exist_ok=True)
    cleaned_filename = f"cleaned_{dataset_id}.csv"
    cleaned_path = os.path.join(settings.processed_dir, cleaned_filename)
    cleaned_df.to_csv(cleaned_path, index=False)

    profile = profile_dataset(cleaned_df)

    dataset.cleaned_path = cleaned_path
    dataset.status = "cleaned"
    dataset.profile_json = json.dumps(profile)
    db.commit()

    return CleaningReport(dataset_id=dataset_id, **report)