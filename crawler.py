import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client

# 1. SETUP: Verbindung zu Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# 2. QUELLEN: Hier fügst du später einfach mehr URLs hinzu
SOURCES = [
    {"url": "https://www.formula1.com/en/racing/2026.html", "cat": "Auto", "sub": "Formel 1"},
    # {"url": "https://www.motogp.com/de/calendar", "cat": "Motorrad", "sub": "MotoGP"},
]

def scrape_f1(source):
    events = []
    response = requests.get(source["url"])
    soup = BeautifulSoup(response.text, 'html.parser')

    # Dies ist ein Beispiel-Selektor. Jede Seite braucht einen eigenen.
    # Wir suchen nach den Renn-Containern
    for race in soup.select('.event-item'): 
        name = race.select_one('.event-title').text.strip()
        # Hier würden wir normalerweise Koordinaten via Geocoding API holen
        # Für den Start nutzen wir statische Test-Koordinaten (Bahrain)
        events.append({
            "name": name,
            "category": source["cat"],
            "description": source["sub"],
            "latitude": 26.032, 
            "longitude": 50.510,
            "price_participation": 0
        })
    return events

def run_crawler():
    all_events = []
    for source in SOURCES:
        print(f"Scanne: {source['url']}")
        if "formula1" in source["url"]:
            all_events.extend(scrape_f1(source))
        
    # Daten in Supabase hochladen
    for event in all_events:
        # Check ob Event schon existiert (optional)
        supabase.table("events").insert(event).execute()
        print(f"Gespeichert: {event['name']}")

if __name__ == "__main__":
    run_crawler()
