import os
from supabase import create_client

def run_crawler():
    # 1. Verbindung zu Supabase herstellen
    # GitHub Actions füllt diese Werte automatisch aus deinen 'Secrets' aus
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        print("Fehler: SUPABASE_URL oder SUPABASE_KEY fehlen in den Secrets!")
        return

    supabase = create_client(url, key)

    # 2. Ein Test-Event vorbereiten
    # Wichtig: Die Spaltennamen (name, category, etc.) müssen exakt so in deiner Tabelle stehen!
    test_event = {
        "name": "Live Test Event",
        "category": "Auto",
        "description": "Crawler Test erfolgreich!",
        "latitude": 52.52,
        "longitude": 13.40,
        "stream_url": "https://youtube.com/live"
    }

    print(f"Versuche Event hochzuladen: {test_event['name']}...")

    # 3. In die Tabelle 'events' einfügen
    try:
        response = supabase.table("events").insert(test_event).execute()
        print("Erfolg! Das Event wurde in Supabase gespeichert.")
        print(response)
    except Exception as e:
        print(f"Fehler beim Hochladen: {e}")

if __name__ == "__main__":
    run_crawler()
