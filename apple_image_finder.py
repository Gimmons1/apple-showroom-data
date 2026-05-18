import json
import os
import time
from duckduckgo_search import DDGS

DB_FILE = "apple_database.json"

def find_images_for_devices():
    print("🔍 Avvio ricerca automatica immagini...")
    
    if not os.path.exists(DB_FILE):
        print(f"Errore: {DB_FILE} non trovato.")
        return

    with open(DB_FILE, "r", encoding="utf-8") as f:
        devices = json.load(f)

    ddgs = DDGS()
    updates = 0

    for device in devices:
        # Cerchiamo solo se non c'è già un'immagine ufficiale e se non c'è una proposta
        if not device.get("imageName") and not device.get("proposedImageUrl"):
            query = f"{device['name']} apple product png transparent background"
            print(f"Cerco immagine per: {device['name']}...")
            
            try:
                # Cerca 1 immagine su DuckDuckGo
                results = list(ddgs.images(query, max_results=1))
                if results:
                    image_url = results[0]['image']
                    device["proposedImageUrl"] = image_url
                    print(f"✅ Trovata: {image_url}")
                    updates += 1
                
                # Pausa per non essere bloccati dal motore di ricerca
                time.sleep(2)
            except Exception as e:
                print(f"❌ Errore ricerca per {device['name']}: {e}")

    if updates > 0:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(devices, f, indent=2, ensure_ascii=False)
        print(f"💾 Salvataggio completato! Aggiunte {updates} proposte di immagini.")
    else:
        print("Nessun nuovo dispositivo necessitava di un'immagine.")

if __name__ == "__main__":
    find_images_for_devices()
