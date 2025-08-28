from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .database import Base

class Cat(Base):
    __tablename__ = "cats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    age_months = Column(Integer, nullable=False)
    weight_g = Column(Integer, nullable=False)
    sex = Column(String, nullable=False)   # "M" / "H"
    stage = Column(String, nullable=True)  # Gatito / Adulto / Gestante / Lactante
    created_at = Column(DateTime, server_default=func.now())

    controls = relationship("Control", back_populates="cat")

class Dewormer(Base):
    __tablename__ = "dewormers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    dose_mg_per_kg = Column(Float, nullable=False)

    controls = relationship("Control", back_populates="dewormer")

class Control(Base):
    __tablename__ = "controls"
    id = Column(Integer, primary_key=True, index=True)
    cat_id = Column(Integer, ForeignKey("cats.id"), nullable=False)
    date = Column(String, nullable=False)  # YYYY-MM-DD
    dewormer_id = Column(Integer, ForeignKey("dewormers.id"), nullable=False)
    total_dose_mg = Column(Float, nullable=False)
    next_control = Column(String, nullable=False)  # YYYY-MM-DD
    notes = Column(String, nullable=True)
    age_months_at_control = Column(Integer, nullable=False)
    weight_g_at_control = Column(Integer, nullable=False)

    cat = relationship("Cat", back_populates="controls")
    dewormer = relationship("Dewormer", back_populates="controls")