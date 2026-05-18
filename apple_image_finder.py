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
        # Cerca solo se non ha un'immagine, non ha una proposta e non ha già fallito in precedenza
        if not device.get("imageName") and not device.get("proposedImageUrl") and not device.get("imageSearchFailed"):
            query = f"{device['name']} apple product png transparent background"
            print(f"Cerco immagine per: {device['name']}...")
            
            try:
                results = list(ddgs.images(query, max_results=1))
                if results:
                    image_url = results[0]['image']
                    device["proposedImageUrl"] = image_url
                    # Se in precedenza aveva fallito ma ora l'ha trovata, rimuoviamo il flag
                    if "imageSearchFailed" in device:
                        del device["imageSearchFailed"]
                    print(f"✅ Trovata: {image_url}")
                else:
                    device["imageSearchFailed"] = True
                    print(f"⚠️ Nessuna immagine trovata per {device['name']}")
                
                updates += 1
                time.sleep(2)
            except Exception as e:
                print(f"❌ Errore ricerca per {device['name']}: {e}")
                device["imageSearchFailed"] = True
                updates += 1

    if updates > 0:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(devices, f, indent=2, ensure_ascii=False)
        print(f"💾 Salvataggio completato! Database aggiornato.")
    else:
        print("Nessun nuovo dispositivo necessitava di un'immagine.")

if __name__ == "__main__":
    find_images_for_devices()
