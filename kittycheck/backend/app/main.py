from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pathlib import Path
from .database import Base, engine, get_db
from . import models, schemas

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="KittyCheck API", version="1.0.0")

# CORS (allow all for demo; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend
frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")

def compute_next_control(edad_meses: int) -> int:
    if edad_meses < 3:
        return 15
    if edad_meses < 6:
        return 30
    return 90

@app.get("/api/dewormers", response_model=list[schemas.DewormerOut])
def list_dewormers(db: Session = Depends(get_db)):
    return db.query(models.Dewormer).order_by(models.Dewormer.name).all()

@app.post("/api/dewormers", response_model=schemas.DewormerOut)
def create_dewormer(payload: schemas.DewormerCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Dewormer).filter(models.Dewormer.name == payload.name).first()
    if existing:
        return existing
    dew = models.Dewormer(name=payload.name, dose_mg_per_kg=payload.dose_mg_per_kg)
    db.add(dew)
    db.commit()
    db.refresh(dew)
    return dew

@app.get("/api/cats", response_model=list[schemas.CatOut])
def list_cats(db: Session = Depends(get_db)):
    return db.query(models.Cat).order_by(models.Cat.created_at.desc()).all()

@app.post("/api/cats", response_model=schemas.CatOut)
def create_cat(payload: schemas.CatCreate, db: Session = Depends(get_db)):
    cat = models.Cat(**payload.dict())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

@app.get("/api/controls", response_model=list[schemas.ControlOut])
def list_controls(db: Session = Depends(get_db)):
    return db.query(models.Control).order_by(models.Control.date.desc()).all()

@app.post("/api/controls", response_model=schemas.ControlOut)
def create_control(payload: schemas.ControlCreate, db: Session = Depends(get_db)):
    cat = None
    if payload.cat_id is not None:
        cat = db.query(models.Cat).get(payload.cat_id)
        if not cat:
            raise HTTPException(status_code=404, detail="Cat not found")
    else:
        if not payload.cat_name:
            raise HTTPException(status_code=400, detail="Provide cat_id or cat_name to create")
        cat = models.Cat(
            name=payload.cat_name,
            age_months=payload.age_months,
            weight_g=payload.weight_g,
            sex=payload.sex,
            stage=payload.stage,
        )
        db.add(cat)
        db.commit()
        db.refresh(cat)

    dew = db.query(models.Dewormer).filter(models.Dewormer.name == payload.dewormer).first()
    if not dew:
        if payload.base_dose_mg_per_kg is None:
            raise HTTPException(status_code=400, detail="New dewormer requires base_dose_mg_per_kg")
        dew = models.Dewormer(name=payload.dewormer, dose_mg_per_kg=payload.base_dose_mg_per_kg)
        db.add(dew)
        db.commit()
        db.refresh(dew)

    weight_kg = payload.weight_g / 1000.0
    base_dose = payload.base_dose_mg_per_kg if payload.base_dose_mg_per_kg is not None else dew.dose_mg_per_kg
    total_dose_mg = round(weight_kg * base_dose, 2)

    interval_days = compute_next_control(payload.age_months)
    date_obj = datetime.strptime(payload.date, "%Y-%m-%d")
    next_date = (date_obj + timedelta(days=interval_days)).strftime("%Y-%m-%d")

    control = models.Control(
        cat_id=cat.id,
        date=payload.date,
        dewormer_id=dew.id,
        total_dose_mg=total_dose_mg,
        next_control=next_date,
        notes=payload.notes or "",
        age_months_at_control=payload.age_months,
        weight_g_at_control=payload.weight_g,
    )
    db.add(control)
    db.commit()
    db.refresh(control)
    return control