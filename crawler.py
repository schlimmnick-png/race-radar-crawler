import os
import requests
import time
from bs4 import BeautifulSoup
from supabase import create_client

# 1. SETUP
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def get_coords(location_name):
    try:
        headers = {'User-Agent': 'RaceRadarBot/1.0'}
        api_url = f"https://nominatim.openstreetmap.org/search?q={location_name}&format=json&limit=1"
        res = requests.get(api_url, headers=headers).json()
        if res: return float(res[0]['lat']), float(res[0]['lon'])
    except: return None, None
    return None, None

# --- SCRAPER FÜR ADAC ---
def scrape_adac():
    events = []
    # Beispiel-URL für den ADAC Kalender (muss ggf. jährlich angepasst werden)
    url = "https://www.adac-motorsport.de/termine/" 
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        # Der ADAC nutzt oft 'cards' oder Tabellenzeilen
        for item in soup.select('.event-card'): # Beispielhafter CSS-Selektor
            name = item.select_one('.title').text.strip()
            loc = item.select_one('.location').text.strip()
            events.append({"name": name, "loc": loc, "cat": "Auto", "desc": "ADAC Event"})
    except Exception as e: print(f"ADAC Fehler: {e}")
    return events

# --- SCRAPER FÜR SPEEDWEEK ---
def scrape_speedweek():
    events = []
    url = "https://www.speedweek.com/kalender"
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        # Speedweek listet Termine oft in Tabellen (tr)
        for row in soup.select('tr.event-row'): 
            name = row.select_one('.event-name').text.strip()
            loc = row.select_one('.venue').text.strip()
            events.append({"name": name, "loc": loc, "cat": "Motorrad", "desc": "Speedweek"})
    except Exception as e: print(f"Speedweek Fehler: {e}")
    return events

def run_crawler():
    # Sammle alle Events von beiden Quellen
    all_found = scrape_adac() + scrape_speedweek()
    
    for event in all_found:
        # 1. Check ob schon in DB (über Name), um Duplikate zu vermeiden
        check = supabase.table("events").select("name").eq("name", event['name']).execute()
        if len(check.data) > 0:
            print(f"Überspringe (existiert bereits): {event['name']}")
            continue

        # 2. Koordinaten finden
        lat, lon = get_coords(event['loc'])
        if lat and lon:
            supabase.table("events").insert({
                "name": event['name'],
                "category": event['cat'],
                "description": event['desc'],
                "latitude": lat,
                "longitude": lon,
                "price_participation": 0
            }).execute()
            print(f"✅ Neu hinzugefügt: {event['name']}")
            time.sleep(1) # Fair Use für Geocoding

if __name__ == "__main__":
    run_crawler()
