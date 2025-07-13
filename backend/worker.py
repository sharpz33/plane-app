# backend/worker.py

from sqlalchemy.orm import Session
from database import SessionLocal
import models

def find_flight_deals():
    """
    Main worker function to find flight deals.
    """
    print("🤖 Worker starting...")
    db: Session = SessionLocal()
    
    try:
        # 1. Get all active alerts from the database
        alerts = db.query(models.Alert).all()
        print(f"🔍 Found {len(alerts)} alerts to process.")

        # 2. Loop through each alert
        for alert in alerts:
            print(f"\nProcessing Alert ID: {alert.id}")
            print(f"  User: {alert.user_email}")
            print(f"  Route: {alert.origin_codes} -> {alert.destination_codes}")
            print(f"  Max Price: {alert.max_price}")
            
            # --- In the next step, we will add the Amadeus API call here ---
    
    finally:
        print("✅ Worker finished.")
        db.close()

if __name__ == "__main__":
    find_flight_deals()