import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.security import get_current_user
from database.models import Dataset, User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary/{dataset_id}")
def get_summary(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id, Dataset.owner_id == current_user.id
    ).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if dataset.status != "cleaned" or not dataset.profile_json:
        raise HTTPException(
            status_code=400,
            detail="Dataset has not been cleaned yet. Call /data/clean/{dataset_id} first.",
        )
    return json.loads(dataset.profile_json)


@router.get("/list")
def list_datasets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    datasets = db.query(Dataset).filter(Dataset.owner_id == current_user.id).all()
    return [
        {"id": d.id, "filename": d.filename, "status": d.status, "created_at": d.created_at}
        for d in datasets
    ]