import json
import requests
import urllib.parse

def build_apple_database():
    url = "https://api.appledb.dev/device/main.json"
    response = requests.get(url)
    data = response.json()
    
    # AppleDB può restituire una lista o un dizionario
    raw_list = data if isinstance(data, list) else list(data.values())
    
    apple_devices = []
    
    for item in raw_list:
        name = item.get("name", "")
        device_type = item.get("type", "")
        
        # FILTRO PULIZIA: Teniamo solo i dispositivi veri e rimuoviamo versioni beta/dev
        valid_types = ["Mac", "iPhone", "iPad", "Watch", "Apple TV", "iPod"]
        if device_type not in valid_types or "beta" in name.lower() or "Developer" in name:
            continue
            
        released = item.get("released", [""])
        release_date = released[0] if isinstance(released, list) and len(released) > 0 else (released if isinstance(released, str) else "")
        year = release_date[:4] if len(release_date) >= 4 else "N/A"
        
        chip = str(item.get("soc", "N/A"))
        category = device_type
        
        # Colori per il design SwiftUI
        theme_color = "#8A8B8C" if "iPhone" in name else ("#007AFF" if "Mac" in name else "#FF2D55")
        
        # --- ESTRAZIONE DATI REALI AL 100% DA APPLEDB ---
        board = item.get("board", [])
        board_str = ", ".join(board) if isinstance(board, list) else str(board)
        
        identifier = item.get("identifier", [])
        ident_str = ", ".join(identifier) if isinstance(identifier, list) else str(identifier)
        
        model = item.get("model", [])
        model_str = ", ".join(model) if isinstance(model, list) else str(model)
        
        arch = str(item.get("arch", "N/A"))
        
        specs = {
            "Rilascio Ufficiale": release_date,
            "Identifier": ident_str,
            "Codice Modello": model_str,
            "Board Config": board_str,
            "Architettura Hardware": arch
        }
        
        # Pulizia: Rimuoviamo i campi vuoti o N/A per non sporcare l'app
        specs = {k: v for k, v in specs.items() if v and v != "N/A" and v != ""}
        
        # --- FIX IMMAGINI ---
        # AppleDB usa la "key" per formare l'URL. Usiamo urllib per convertire gli spazi.
        key = item.get("key", "")
        image_key = urllib.parse.quote(key)
        image_url = f"https://img.appledb.dev/device@256/{image_key}/0.png"
        
        apple_devices.append({
            "id": key,
            "name": name,
            "chip": chip,
            "releaseYear": year,
            "category": category,
            "imageURL": image_url,
            "themeColor": theme_color,
            "specs": specs
        })
        
    # Ordinamento cronologico decrescente
    apple_devices.sort(key=lambda x: str(x["releaseYear"]), reverse=True)
    
    with open("apple_database.json", "w", encoding="utf-8") as f:
        json.dump(apple_devices, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    build_apple_database()
