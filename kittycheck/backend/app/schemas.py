from pydantic import BaseModel, Field
from typing import Optional

class DewormerBase(BaseModel):
    name: str

class DewormerCreate(DewormerBase):
    dose_mg_per_kg: float = Field(..., gt=0)

class DewormerOut(DewormerBase):
    id: int
    dose_mg_per_kg: float
    class Config:
        from_attributes = True

class CatBase(BaseModel):
    name: str
    age_months: int
    weight_g: int
    sex: str
    stage: Optional[str] = None

class CatCreate(CatBase):
    pass

class CatOut(CatBase):
    id: int
    class Config:
        from_attributes = True

class ControlCreate(BaseModel):
    cat_id: Optional[int] = None
    cat_name: Optional[str] = None
    age_months: int
    weight_g: int
    sex: str
    stage: Optional[str] = None
    dewormer: str
    base_dose_mg_per_kg: Optional[float] = None
    date: str  # YYYY-MM-DD
    notes: Optional[str] = None

class ControlOut(BaseModel):
    id: int
    cat_id: int
    date: str
    total_dose_mg: float
    next_control: str
    notes: Optional[str] = None
    age_months_at_control: int
    weight_g_at_control: int
    dewormer_id: int
    class Config:
        from_attributes = True