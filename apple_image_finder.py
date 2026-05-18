import json
import os
import time
from duckduckgo_search import DDGS

DB_FILE = "apple_database.json"

def find_images_for_devices():
    print("🔍 Avvio ricerca automatica immagini avanzata...")
    
    if not os.path.exists(DB_FILE):
        print(f"Errore: {DB_FILE} non trovato.")
        return

    with open(DB_FILE, "r", encoding="utf-8") as f:
        devices = json.load(f)

    ddgs = DDGS()
    updates = 0

    for device in devices:
        # Cerca solo se non ha un'immagine definitiva, non ha proposte e non ha fallito di recente
        if not device.get("imageName") and not device.get("proposedImageUrls") and not device.get("proposedImageUrl") and not device.get("imageSearchFailed"):
            name = device['name']
            print(f"Cerco immagini per: {name}...")
            
            # Ampliamo le parole chiave per avere più possibilità di trovare immagini buone
            queries = [
                f"{name} apple png transparent background",
                f"{name} apple device png",
                f"Apple {name} computer white background"
            ]
            
            found_urls = []
            
            try:
                for q in queries:
                    if len(found_urls) >= 3: # Vogliamo proporre al massimo 3 immagini
                        break
                    
                    results = list(ddgs.images(q, max_results=3))
                    for res in results:
                        if res['image'] not in found_urls:
                            found_urls.append(res['image'])
                        if len(found_urls) >= 3:
                            break
                    time.sleep(1) # Pausa per non bloccare il motore di ricerca
                
                if found_urls:
                    device["proposedImageUrls"] = found_urls
                    if "imageSearchFailed" in device:
                        del device["imageSearchFailed"]
                    print(f"✅ Trovate {len(found_urls)} immagini per {name}")
                else:
                    device["imageSearchFailed"] = True
                    print(f"⚠️ Nessuna immagine trovata per {name}")
                
                updates += 1
            except Exception as e:
                print(f"❌ Errore ricerca per {name}: {e}")
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
