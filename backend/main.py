from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from amadeus import Client

import crud
import models
import schemas
import location_resolver
from database import engine, SessionLocal
from config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Plane! App")

amadeus = Client(
    client_id=settings.AMADEUS_API_KEY,
    client_secret=settings.AMADEUS_API_SECRET,
    hostname='test'
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Plane! ✈️"}

@app.post("/alerts/", response_model=schemas.Alert)
def create_new_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    origin_codes = location_resolver.get_iata_codes(db, amadeus, alert.origin_codes)
    destination_codes = location_resolver.get_iata_codes(db, amadeus, alert.destination_codes)

    if not origin_codes:
        raise HTTPException(status_code=404, detail=f"Origin location '{alert.origin_codes}' not found.")
    if not destination_codes:
        raise HTTPException(status_code=404, detail=f"Destination location '{alert.destination_codes}' not found.")

    alert_to_create = alert.model_copy(update={
        "origin_codes": origin_codes,
        "destination_codes": destination_codes
    })
    
    return crud.create_alert(db=db, alert=alert_to_create)