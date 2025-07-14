import streamlit as st
import requests

# Adres URL naszego backendu w sieci Docker
BACKEND_URL = "http://backend:8000/alerts/"

st.set_page_config(page_title="Plane! App", page_icon="✈️")

st.title("✈️ Plane! App")
st.header("Set Up a New Flight Alert")

with st.form(key="alert_form"):
    # Form fields
    email = st.text_input(label="Your Email Address")
    origin = st.text_input(label="Origin (City or Country)")
    destination = st.text_input(label="Destination (City or Country)")
    
    col1, col2 = st.columns(2)
    with col1:
        date_from = st.date_input(label="Search From")
    with col2:
        date_to = st.date_input(label="Search To")
    
    max_price = st.number_input(label="Max Price (EUR)", min_value=0)
    
    submit_button = st.form_submit_button(label="Set Alert")

# Handle form submission
if submit_button:
    if not all([email, origin, destination, date_from, date_to, max_price]):
        st.warning("Please fill in all required fields.")
    else:
        alert_data = {
            "user_email": email,
            "origin_codes": origin,
            "destination_codes": destination,
            "departure_date_from": str(date_from),
            "departure_date_to": str(date_to),
            "max_price": max_price,
        }
        
        try:
            with st.spinner("Setting up your alert..."):
                response = requests.post(BACKEND_URL, json=alert_data)
                
                if response.status_code == 200:
                    st.success("✅ Alert set up successfully! We'll notify you about the best deals.")
                else:
                    st.error(f"❌ Error setting alert: {response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Could not connect to the backend: {e}")