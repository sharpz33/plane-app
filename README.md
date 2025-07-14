## Plane! ✈️
Plane! is a self-hosted, open-source flight deal finder designed to automatically hunt for the cheapest flights based on your personalized, flexible criteria.

Tired of manually searching for deals every day? Set up a highly specific alert and let Plane! do the work for you. Get notified via email (and more channels to come!) when a flight matching your budget is found.

### Key Features (Target Vision)
- Flexible Alerts: Search from specific cities, entire countries, or a list of your favorite airports.
- Advanced Date Options: Define a fixed date range, a flexible stay duration (e.g., a 7-10 day trip in October), or a rolling search window (e.g., "any weekend in the next 3 months").
- Price Tracking: Set your max price and get notified only when the price is right.
- Multi-Provider Strategy: Aggregates data from multiple sources to find the best possible deals.
- Extensible Notifications: Receive alerts via email, with plans for Pushbullet, Telegram, and more.
- Self-Hosted & Private: All your alerts and data are stored locally on your server, under your control.

### Current Status
This project is currently at the **MVP (Minimum Viable Product)** stage. The core functionality is complete:
- Users can create alerts via an API endpoint.
- A worker process automatically searches for flights using the Amadeus API based on saved alerts.
- Email notifications are sent when a matching deal is found.

The next steps involve building a user interface for managing alerts and expanding the notification and search capabilities.