import json
import os

DB_FILE = "apple_database.json"

def clean_and_sort_db():
    print("🍏 Avvio manutenzione del database Apple Showroom...")

    if not os.path.exists(DB_FILE):
        print(f"⚠️ File {DB_FILE} non trovato. Ne creo uno vuoto.")
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return

    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            devices = json.load(f)
        except json.JSONDecodeError:
            print("❌ Errore: Il file JSON è corrotto! Intervento manuale richiesto.")
            return

    # Rimuove i duplicati (mantiene sempre l'ultima versione inviata dall'App Admin)
    unique_devices = {}
    for device in devices:
        unique_devices[device["id"]] = device

    clean_list = list(unique_devices.values())

    # Ordina i dispositivi in modo decrescente (dai più nuovi ai più vecchi)
    def get_year(device):
        year_str = device.get("releaseYear", "0")
        clean_year = ''.join(filter(str.isdigit, year_str))
        return int(clean_year) if clean_year else 0

    clean_list.sort(key=get_year, reverse=True)

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(clean_list, f, indent=2, ensure_ascii=False)

    print(f"✅ Database ottimizzato e formattato! Totale dispositivi in vetrina: {len(clean_list)}")

if __name__ == "__main__":
    clean_and_sort_db()
