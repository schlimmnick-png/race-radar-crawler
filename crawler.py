name: Racing Crawler

on:
  schedule:
    - cron: '0 0 * * *' # Läuft einmal täglich
  workflow_dispatch: # Erlaubt manuelles Starten

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Code auschecken
        uses: actions/checkout@v3

      - name: Python installieren
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Abhängigkeiten installieren
        run: |
          pip install supabase
          # Falls du andere Bibliotheken wie 'requests' nutzt, hier hinzufügen:
          # pip install requests 

      - name: Crawler ausführen
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
        run: python crawler.py # Hier muss der Name deiner Datei stehen!
