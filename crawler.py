
import os
import requests
import time
from supabase import create_client

# 1. SETUP
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# 2. GEOCODING FUNKTION (Verwandelt Text in GPS-Daten)
def get_coords(location_name):
    try:
        # Wir fragen OpenStreetMap nach den Koordinaten
        headers = {'User-Agent': 'RaceRadarBot/1.0'}
        api_url = f"https://nominatim.openstreetmap.org/search?q={location_name}&format=json&limit=1"
        response = requests.get(api_url, headers=headers).json()
        if response:
            return float(response[0]['lat']), float(response[0]['lon'])
    except Exception as e:
        print(f"Fehler beim Geocoding für {location_name}: {e}")
    return None, None

def run_crawler():
    # BEISPIEL: Eine Liste von Events, die wir von verschiedenen Seiten "gefunden" haben
    # Später wird dieser Teil durch echte Scraping-Logik für jede Seite ersetzt
    found_events = [
        {"name": "MX Masters Fürstlich Drehna", "loc": "Fürstlich Drehna", "cat": "Motorrad", "desc": "Motocross"},
        {"name": "24h Nürburgring", "loc": "Nürburgring", "cat": "Auto", "desc": "Trackday"},
        {"name": "SimRacing Expo", "loc": "Messe Dortmund", "cat": "Sim Racing", "desc": "Messe"}
    ]

    for event in found_events:
        print(f"Verarbeite: {event['name']}...")
        
        # GPS Daten holen
        lat, lon = get_coords(event['loc'])
        
        if lat and lon:
            # In Supabase speichern
            new_data = {
                "name": event['name'],
                "category": event['cat'],
                "description": event['desc'],
                "latitude": lat,
                "longitude": lon,
                "price_participation": 0
            }
            
            # Hochladen (Duplikat-Check wäre hier sinnvoll)
            supabase.table("events").insert(new_data).execute()
            print(f"✅ Erfolg: {event['name']} auf Karte gesetzt ({lat}, {lon})")
            
            # WICHTIG: Die API erlaubt nur 1 Anfrage pro Sekunde (Fair Use)
            time.sleep(1)
        else:
            print(f"❌ Standort nicht gefunden für: {event['loc']}")

if __name__ == "__main__":
    run_crawler()
