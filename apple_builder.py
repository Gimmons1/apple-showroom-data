import json
import requests

def build_apple_database():
    url = "https://api.appledb.dev/device/main.json"
    response = requests.get(url)
    data = response.json()
    raw_list = data if isinstance(data, list) else list(data.values())

    
    apple_devices = []
    
    for item in raw_list:
        name = item.get("name", "")
        device_type = item.get("type", "")
        
        # Filtriamo solo i dispositivi reali (niente beta)
        if device_type not in ["Mac", "iPhone", "iPad"] or "beta" in name.lower():
            continue
            
        released = item.get("released", [""])
        release_date = released[0] if isinstance(released, list) and len(released) > 0 else (released if isinstance(released, str) else "")
        year = release_date[:4] if len(release_date) >= 4 else "Sconosciuto"
        
        # 🚨 NESSUN LIMITE DI ANNO! Prendiamo TUTTO dal 1984 a oggi.
        
        chip = str(item.get("soc", "Apple / Intel / Moto"))
        category = device_type
        
        # Colori dinamici per il Liquid Glass
        theme_color = "#8A8B8C" if "iPhone" in name else ("#007AFF" if "Mac" in name else "#FF2D55")
        
        # Costruttore URL Immagine
        identifier = item.get("identifier", "")
        ident_str = identifier[0] if isinstance(identifier, list) else str(identifier)
        image_url = f"https://img.appledb.dev/device@{ident_str}/0.png"
        
        specs = {
            "Introduced": release_date,
            "Model ID": ident_str
        }
        
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
        
    # Ordiniamo dal più recente al più antico
    apple_devices.sort(key=lambda x: str(x["releaseYear"]), reverse=True)
    
    with open("apple_database.json", "w", encoding="utf-8") as f:
        json.dump(apple_devices, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    build_apple_database()
