from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(Float, default=datetime.utcnow().timestamp, nullable=False)

    # Relationship to CarbonFootprint
    carbon_footprints = relationship("CarbonFootprint", back_populates="user")


class CarbonFootprint(Base):
    __tablename__ = 'carbon_footprints'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(Float, default=datetime.utcnow().timestamp, nullable=False)
    
    # Emissions by scope
    scope1_emissions = Column(Float, nullable=False)  # Direct emissions
    scope2_emissions = Column(Float, nullable=False)  # Indirect emissions from energy
    scope3_emissions = Column(Float, nullable=False)  # Other indirect emissions
    total_emissions = Column(Float, nullable=False)   # Total carbon footprint
    
    # Detailed emission data
    emission_details = Column(JSON, nullable=False)   # Stores detailed breakdown by category
    
    # Relationship to User
    user = relationship("User", back_populates="carbon_footprints")