from amadeus import Client, ResponseError
from sqlalchemy.orm import Session
import models

def get_iata_codes(db: Session, amadeus_client: Client, location_name: str) -> str | None:
    search_term_lower = location_name.lower()
    cached_location = db.query(models.LocationCache).filter(models.LocationCache.search_term == search_term_lower).first()
    
    if cached_location:
        print(f"CACHE HIT: Found '{location_name}' in local cache.")
        return cached_location.iata_codes

    print(f"CACHE MISS: '{location_name}' not found locally. Querying Amadeus API.")
    
    try:
        response = amadeus_client.reference_data.locations.get(
            keyword=location_name,
            subType='AIRPORT,CITY'
        )
        codes = [location['iataCode'] for location in response.data]
        
        if not codes:
            return None

        iata_codes_str = ",".join(codes)
        db_cache_entry = models.LocationCache(search_term=search_term_lower, iata_codes=iata_codes_str)
        db.add(db_cache_entry)
        db.commit()
        db.refresh(db_cache_entry)
        
        print(f"SAVED TO CACHE: '{location_name}' -> '{iata_codes_str}'")
        return iata_codes_str

    except ResponseError as error:
        print(f"Amadeus location search error: {error}")
        return None