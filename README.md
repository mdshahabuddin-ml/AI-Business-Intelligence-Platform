# AI Business Intelligence Platform

An AI-powered platform that transforms raw business data (CSV/Excel) into automatic cleaning, dashboards, ML predictions, forecasts, and natural-language insights.

## Status: Milestone 1 Complete

- JWT authentication (register/login)
- Dataset upload with validation (CSV/Excel)
- Automatic data cleaning (duplicates, missing values, type fixes, outlier detection)
- EDA dashboard with KPIs, correlations, categorical summaries
- Tested with pytest (7/7 tests passing)

## Tech Stack

- Backend: FastAPI, SQLAlchemy, Pydantic
- Data Processing: pandas, numpy
- Auth: JWT (python-jose), bcrypt password hashing
- Testing: pytest

## Setup

python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.main:app --reload

Visit http://127.0.0.1:8000/docs for the interactive API documentation.

## Run Tests

python -m pytest tests/unit/ -v

## Project Structure

backend/          FastAPI app: auth, upload, dashboard routes
data_pipeline/     Data validation and cleaning logic
database/          SQLAlchemy models
tests/             Unit tests
storage/           Uploaded and processed files

## Roadmap

- [x] Milestone 1: Auth, upload, cleaning, dashboard
- [ ] Milestone 2: ML models (regression, forecasting, anomaly detection)
- [ ] Milestone 3: LLM integration (chat-with-data, business insights)
- [ ] Milestone 4: Docker deployment, CI/CD

## Author

Md Shahabuddin
