# backend/worker.py

from sqlalchemy.orm import Session
from amadeus import Client, ResponseError
from database import SessionLocal
from config import settings
import models
import crud

def find_flight_deals():
    """
    Main worker function to find flight deals and check if they are new.
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
                
                print(f"  -> Searching for all destinations from: {origin}")
                
                try:
                    response = amadeus.shopping.flight_destinations.get(origin=origin)
                    
                    if not response.data: continue

                    for flight in response.data:
                        destination = flight['destination']
                        price = float(flight['price']['total'])

                        # Check if the found flight matches the alert criteria
                        if destination in destination_codes and price <= alert.max_price:
                            
                            # Create a unique hash for this specific deal
                            deal_hash = f"{alert.id}-{origin}-{destination}-{flight['departureDate']}-{price}"
                            
                            # Check if we have already notified about this deal
                            existing_deal = crud.get_notified_deal_by_hash(db, deal_hash=deal_hash)
                            
                            if existing_deal:
                                print(f"    INFO: Deal {origin}->{destination} for {price} EUR already notified. Skipping.")
                                continue

                            # --- NEW DEAL FOUND ---
                            print(f"    ✅ NEW DEAL FOUND! {origin} -> {destination} for {price} EUR.")
                            
                            # Save this deal to our 'memory' so we don't notify again
                            crud.create_notified_deal(db, alert_id=alert.id, deal_hash=deal_hash, price=price)
                            
                            # In the next step, we will send an email here

                except ResponseError as error:
                    print(f"    INFO: No inspiration flights found for {origin}. Reason: {error.code}")
    
    finally:
        print("\n✅ Worker finished.")
        db.close()

if __name__ == "__main__":
    find_flight_deals()