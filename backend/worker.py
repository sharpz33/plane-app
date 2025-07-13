# backend/worker.py

from sqlalchemy.orm import Session
from amadeus import Client, ResponseError
from database import SessionLocal
from config import settings
import models

def find_flight_deals():
    """
    Main worker function to find flight deals using the efficient
    Flight Inspiration Search API.
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

            # Loop ONLY through origins, making one API call per origin
            for origin in origin_codes:
                if not origin:
                    continue
                
                print(f"  -> Searching for all destinations from: {origin}")
                
                try:
                    # Use the Flight Inspiration Search API
                    response = amadeus.shopping.flight_destinations.get(
                        origin=origin,
                        # We can add departureDate, oneWay, etc. later
                    )
                    
                    if not response.data:
                        continue

                    # Now, we filter the results locally
                    for flight in response.data:
                        if flight['destination'] in destination_codes and float(flight['price']['total']) <= alert.max_price:
                            print(f"    ✅ SUCCESS! Found a deal: {origin} -> {flight['destination']} for {flight['price']['total']} EUR.")
                            # In the next step, we will process this deal

                except ResponseError as error:
                    print(f"    INFO: No inspiration flights found for {origin}. Reason: {error.code}")
    
    finally:
        print("\n✅ Worker finished.")
        db.close()

if __name__ == "__main__":
    find_flight_deals()