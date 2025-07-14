# backend/notifications.py

import requests
from config import settings

def send_deal_email(recipient_email: str, deal_info: dict) -> bool:
    """
    Sends an email notification using the Mailgun HTTP API.
    """
    subject = f"✈️ New Flight Deal Found: {deal_info['origin']} -> {deal_info['destination']}"
    body = f"""
    Hello!
    
    We found a new flight deal matching your alert:
    
    From: {deal_info['origin']}
    To: {deal_info['destination']}
    Price: {deal_info['price']} EUR
    Departure Date: {deal_info['departureDate']}
    
    Happy travels!
    - Plane! App
    """
    
    # Mailgun API endpoint URL for your domain
    api_url = f"https://api.eu.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages"
    
    # Sender's address
    sender_address = f"Plane! App <alerts@{settings.MAILGUN_DOMAIN}>"

    try:
        response = requests.post(
            api_url,
            auth=("api", settings.MAILGUN_API_KEY),
            data={
                "from": sender_address,
                "to": [recipient_email],
                "subject": subject,
                "text": body
            }
        )
        
        # Raise an exception if the request failed
        response.raise_for_status()
        
        print(f"    📬 Email notification sent successfully via Mailgun API to {recipient_email}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"    ❌ Failed to send email via Mailgun API to {recipient_email}.")
        if e.response is not None:
            print(f"    Response Status: {e.response.status_code}")
            print(f"    Response Body: {e.response.text}")
        else:
            print(f"    Error: {e}")
        return False