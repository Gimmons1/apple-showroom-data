import json
import os
import urllib.request

DB_FILE = "apple_database.json"

def check_image_links():
    print("🛡️ Avvio controllo link immagini...")
    
    if not os.path.exists(DB_FILE):
        print(f"Errore: {DB_FILE} non trovato.")
        return

    with open(DB_FILE, "r", encoding="utf-8") as f:
        devices = json.load(f)

    updates = 0

    for device in devices:
        img_url = device.get("imageName")
        
        # Controlla solo i link esterni, ignora le immagini locali di vecchie versioni
        if img_url and img_url.startswith("http"):
            try:
                # Facciamo una richiesta "HEAD" leggerissima solo per vedere se il server risponde 200 OK
                req = urllib.request.Request(img_url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.status != 200:
                        raise Exception("Status non 200")
            except Exception as e:
                print(f"❌ Link ROTTO per {device['name']}: {img_url} ({e})")
                # Segnaliamo il problema rimuovendo il link e impostando il flag
                device["imageName"] = None
                device["imageSearchFailed"] = True
                updates += 1

    if updates > 0:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(devices, f, indent=2, ensure_ascii=False)
        print(f"⚠️ Trovati {updates} link rotti. Database aggiornato per richiedere nuove immagini.")
    else:
        print("✅ Tutti i link delle immagini sono sani e funzionanti!")

if __name__ == "__main__":
    check_image_links()
