from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.api import auth, upload, dashboard
from database import models  # noqa: F401  (registers models before create_all)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Business Intelligence Platform",
    description="Milestone 1: Auth, dataset upload, automatic cleaning, and EDA dashboard.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {"message": "AI Business Intelligence Platform API is running", "docs": "/docs"}