import json
import requests
import urllib.parse

def get_enriched_specs(name, category, chip, year, model_str, board_str):
    # Dati base grezzi di AppleDB
    specs = {
        "Codice Modello": model_str,
        "Scheda Madre": board_str,
        "Architettura": "64-bit ARM" if ("A" in chip or "M" in chip) else "x86 Intel / Altro"
    }

    # Motore di Arricchimento Specifiche Commerciali (Stile Mactracker)
    if category == "iPhone":
        specs["Sistema Operativo"] = "iOS"
        specs["Connettore"] = "USB-C" if ("15" in name or "16" in name) else "Lightning"
        specs["Sicurezza"] = "Face ID" if any(x in name for x in ["X", "11", "12", "13", "14", "15", "16"]) else "Touch ID"
        specs["Display"] = "Super Retina XDR OLED" if "Pro" in name else ("Liquid Retina IPS" if int(year[:4]) < 2020 else "OLED")
    
    elif category == "Mac":
        specs["Sistema Operativo"] = "macOS"
        if "Air" in name:
            specs["Design"] = "Fanless (Senza ventola)"
        if "Pro" in name:
            specs["Display"] = "Liquid Retina XDR (Mini-LED)" if ("M1" in chip or "M2" in chip or "M3" in chip) else "Retina Display"
            
    elif category == "iPad":
        specs["Sistema Operativo"] = "iPadOS"
        specs["Display"] = "Tandem OLED / Liquid Retina" if "Pro" in name else "Retina Display"
        specs["Sicurezza"] = "Face ID" if "Pro" in name else "Touch ID"

    # Rimuoviamo campi vuoti
    return {k: v for k, v in specs.items() if v and v != "N/A" and v != ""}

def build_apple_database():
    url = "https://api.appledb.dev/device/main.json"
    response = requests.get(url)
    data = response.json()
    
    raw_list = data if isinstance(data, list) else list(data.values())
    apple_devices = []
    
    for item in raw_list:
        name = item.get("name", "")
        device_type = item.get("type", "")
        
        # 🚨 FILTRO ANTI-SPAZZATURA: Rimuoviamo dispositivi fantasma, non rilasciati o simulatori
        if device_type not in ["Mac", "iPhone", "iPad", "Watch"]:
            continue
        if any(bad_word in name.lower() for bad_word in ["beta", "unreleased", "simulator", "developer", "unknown", "internal"]):
            continue
            
        released = item.get("released", [""])
        release_date = released[0] if isinstance(released, list) and len(released) > 0 else (released if isinstance(released, str) else "")
        year = release_date[:4] if len(release_date) >= 4 else "N/A"
        
        # Saltiamo i modelli che non hanno una data ufficiale
        if year == "N/A":
            continue
            
        chip = str(item.get("soc", "N/A"))
        category = device_type
        theme_color = "#8A8B8C" if "iPhone" in name else ("#007AFF" if "Mac" in name else "#FF2D55")
        
        # Estrazione Identificatori per le immagini e i dati
        identifier = item.get("identifier", [])
        ident_list = identifier if isinstance(identifier, list) else [identifier]
        ident_str = ", ".join(ident_list)
        
        # Usiamo il primissimo identificatore (es. iPhone15,2) per cercare l'immagine ufficiale
        first_ident = ident_list[0] if ident_list else item.get("key", "")
        image_key = urllib.parse.quote(str(first_ident))
        image_url = f"https://img.appledb.dev/device@256/{image_key}/0.png"
        
        board = item.get("board", [])
        board_str = ", ".join(board) if isinstance(board, list) else str(board)
        model = item.get("model", [])
        model_str = ", ".join(model) if isinstance(model, list) else str(model)
        
        # Uniamo tutto
        specs = get_enriched_specs(name, category, chip, year, model_str, board_str)
        specs["Rilascio Ufficiale"] = release_date
        specs["Identifier"] = ident_str
        
        apple_devices.append({
            "id": item.get("key", name.replace(" ", "-").lower()),
            "name": name,
            "chip": chip,
            "releaseYear": year,
            "category": category,
            "imageURL": image_url,
            "themeColor": theme_color,
            "specs": specs
        })
        
    apple_devices.sort(key=lambda x: str(x["releaseYear"]), reverse=True)
    
    with open("apple_database.json", "w", encoding="utf-8") as f:
        json.dump(apple_devices, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    build_apple_database()
