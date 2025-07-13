# backend/main.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import crud
import schemas
from database import SessionLocal

# Import components from our project
import models
from database import engine

# This line is the magic part: it reads all the table definitions
# from models.py and creates them in the database if they don't exist.
models.Base.metadata.create_all(bind=engine)

# Dependency to get a DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize the FastAPI app
app = FastAPI(title="Plane! App")


@app.post("/alerts/", response_model=schemas.Alert)
def create_new_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    # Na razie pomijamy walidację kodów lotnisk, zrobimy to później
    return crud.create_alert(db=db, alert=alert)


@app.get("/")
def read_root():
    """
    Root endpoint to check if the application is running.
    """
    return {"message": "Welcome to Plane! ✈️ The database should be initialized."}
