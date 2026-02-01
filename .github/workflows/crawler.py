import os
import requests
from supabase import create_client

# Verbindung zu deiner DB
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def crawl_and_upload():
    # Beispiel: Hier könnten wir eine echte URL scrapen
    # Für den Start erstellen wir ein "virtuelles" Event zum Testen
    new_event = {
        "name": "Formula 1 Test Event",
        "category": "Auto",
        "description": "F1 Live",
        "latitude": 52.5207,
        "longitude": 13.4094,
        "price_participation": 0
    }

    # In Supabase hochladen
    data, count = supabase.table("events").insert(new_event).execute()
    print(f"Erfolg: {data}")

if __name__ == "__main__":
    crawl_and_upload()
