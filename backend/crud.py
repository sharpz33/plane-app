# backend/crud.py

from sqlalchemy.orm import Session
import models
import schemas

# --- Istniejąca funkcja ---
def create_alert(db: Session, alert: schemas.AlertCreate):
    db_alert = models.Alert(**alert.model_dump())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

# --- Nowe funkcje ---
def get_notified_deal_by_hash(db: Session, deal_hash: str):
    return db.query(models.NotifiedDeal).filter(models.NotifiedDeal.flight_offer_hash == deal_hash).first()

def create_notified_deal(db: Session, alert_id: int, deal_hash: str, price: float):
    db_deal = models.NotifiedDeal(
        alert_id=alert_id,
        flight_offer_hash=deal_hash,
        notified_price=price
    )
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    return db_deal