# backend/worker.py

from sqlalchemy.orm import Session
from amadeus import Client, ResponseError
from database import SessionLocal
from config import settings
import models
import crud
import notifications
import time

def find_flight_deals():
    """
    Main worker function to find flight deals and notify users.
    """
    print("🤖 Worker starting with SMART SEARCH...")
    db: Session = SessionLocal()

    amadeus = Client(
        client_id=settings.AMADEUS_API_KEY,
        client_secret=settings.AMADEUS_API_SECRET,
        hostname='test'
    )
    print("✅ Amadeus client initialized.")

    try:
        alerts = db.query(models.Alert).all()
        print(f"🔍 Found {len(alerts)} alerts to process.")

        for alert in alerts:
            print(f"\nProcessing Alert ID: {alert.id} for {alert.user_email}")
            
            origin_codes = set(alert.origin_codes.split(','))
            destination_codes = set(alert.destination_codes.split(','))

            for origin in origin_codes:
                if not origin: continue
                # Be a good API citizen: wait 1 second between requests
                time.sleep(1)                
                
                print(f"  -> Searching for all destinations from: {origin}")
                
                try:
                    response = amadeus.shopping.flight_destinations.get(origin=origin)
                    
                    if not response.data: continue

                    for flight in response.data:
                        destination = flight['destination']
                        price = float(flight['price']['total'])

                        if destination in destination_codes and price <= alert.max_price:
                            deal_hash = f"{alert.id}-{origin}-{destination}-{flight['departureDate']}-{price}"
                            existing_deal = crud.get_notified_deal_by_hash(db, deal_hash=deal_hash)
                            
                            if existing_deal:
                                continue

                            print(f"    ✅ NEW DEAL FOUND! {origin} -> {destination} for {price} EUR.")
                            
                            deal_data = {
                                "origin": origin,
                                "destination": destination,
                                "price": price,
                                "departureDate": flight['departureDate']
                            }
                            
                            # --- CORRECT LOGIC ---
                            # 1. First, try to send the email.
                            email_sent = notifications.send_deal_email(alert.user_email, deal_data)
                            
                            # 2. Only if the email was sent successfully, save to the database.
                            if email_sent:
                                crud.create_notified_deal(db, alert_id=alert.id, deal_hash=deal_hash, price=price)
                                print(f"    💾 Deal information saved to database.")

                except ResponseError as error:
                    print(f"    INFO: No inspiration flights found for {origin}. Reason: {error.code}")
    
    finally:
        print("\n✅ Worker finished.")
        db.close()

if __name__ == "__main__":
    find_flight_deals()