from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True, nullable=False)
    origin_codes = Column(String, nullable=False)
    destination_codes = Column(String, nullable=False)
    departure_date_from = Column(String, nullable=False)
    departure_date_to = Column(String, nullable=False)
    stay_duration_from = Column(Integer)
    stay_duration_to = Column(Integer)
    max_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    notified_deals = relationship("NotifiedDeal", back_populates="alert")

class NotifiedDeal(Base):
    __tablename__ = "notified_deals"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    flight_offer_hash = Column(String, unique=True, index=True, nullable=False)
    notified_price = Column(Float, nullable=False)
    notified_at = Column(DateTime, default=datetime.utcnow)
    alert = relationship("Alert", back_populates="notified_deals")

class LocationCache(Base):
    __tablename__ = "location_cache"

    id = Column(Integer, primary_key=True, index=True)
    search_term = Column(String, unique=True, index=True, nullable=False)
    iata_codes = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)