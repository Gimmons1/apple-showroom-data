import json
import os
import time
import urllib.request
import urllib.parse
from duckduckgo_search import DDGS

DB_FILE = "apple_database.json"

def clean_name_for_search(name):
    # Rimuove le doppie versioni (es. "Apple III / Apple III Plus" -> "Apple III")
    name = name.split('/')[0].strip()
    # Rimuove eventuali dettagli tra parentesi
    name = name.split('(')[0].strip()
    return name

def search_wikipedia_image(clean_name):
    # Interroga direttamente le API di Wikipedia in inglese
    wiki_title = urllib.parse.quote(clean_name)
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={wiki_title}&prop=pageimages&format=json&pithumbsize=800"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            pages = data.get("query", {}).get("pages", {})
            for page_id, page_data in pages.items():
                if "thumbnail" in page_data:
                    return page_data["thumbnail"]["source"]
    except Exception as e:
        print(f"Errore Wikipedia per {clean_name}: {e}")
    return None

def find_images_for_devices():
    print("🔍 Avvio ricerca automatica immagini POTENZIATA (Wikipedia + DDG)...")
    
    if not os.path.exists(DB_FILE):
        print(f"Errore: {DB_FILE} non trovato.")
        return

    with open(DB_FILE, "r", encoding="utf-8") as f:
        devices = json.load(f)

    try:
        ddgs = DDGS()
    except Exception as e:
        ddgs = None
        print(f"Attenzione: Errore inizializzazione DDGS: {e}")

    updates = 0

    for device in devices:
        # Cerca solo se non ha un'immagine, non ha proposte e non ha fallito di recente
        if not device.get("imageName") and not device.get("proposedImageUrls") and not device.get("proposedImageUrl") and not device.get("imageSearchFailed"):
            raw_name = device['name']
            clean_name = clean_name_for_search(raw_name)
            print(f"\nCerco immagini per: '{raw_name}' (Usando chiave: '{clean_name}')")
            
            found_urls = []
            
            # 1. TENTATIVO: Wikipedia (altissima priorità e affidabilità)
            wiki_img = search_wikipedia_image(clean_name)
            if wiki_img:
                print(f"   [+] Immagine trovata su Wikipedia!")
                found_urls.append(wiki_img)
            
            # Se il nome è troppo corto (es. "MacBook"), aggiungiamo Apple per sicurezza su DuckDuckGo
            search_term = clean_name
            if "Apple" not in search_term and "Mac" not in search_term and "iPhone" not in search_term and "iPad" not in search_term:
                search_term = f"Apple {search_term}"

            # 2. TENTATIVI: DuckDuckGo con query progressive e morbide
            queries = [
                f"{search_term} hardware png transparent",
                f"{search_term} computer white background",
                f"{search_term} apple device"
            ]
            
            if ddgs:
                for q in queries:
                    if len(found_urls) >= 3:
                        break # Abbiamo già 3 immagini
                    print(f"   [-] Provo query DDG: {q}")
                    try:
                        results = list(ddgs.images(q, max_results=3))
                        for res in results:
                            if res['image'] not in found_urls:
                                found_urls.append(res['image'])
                            if len(found_urls) >= 3:
                                break
                        time.sleep(1.5) # Pausa per non bloccare il motore di ricerca
                    except Exception as e:
                        print(f"   [x] Errore DDG: {e}")

            if found_urls:
                device["proposedImageUrls"] = found_urls[:3] # Salva fino a un massimo di 3 immagini
                if "imageSearchFailed" in device:
                    del device["imageSearchFailed"]
                print(f"✅ TOTALE: Trovate {len(device['proposedImageUrls'])} immagini.")
            else:
                device["imageSearchFailed"] = True
                print(f"⚠️ NESSUNA immagine trovata in tutto il web.")
            
            updates += 1

    if updates > 0:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(devices, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Salvataggio completato! Database aggiornato.")
    else:
        print("\nNessun nuovo dispositivo necessitava di un'immagine.")

if __name__ == "__main__":
    find_images_for_devices()
