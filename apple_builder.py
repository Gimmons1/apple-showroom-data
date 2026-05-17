import json
import requests
import urllib.parse

def get_commercial_specs(name, key, chip, year):
    # Specifiche di base ereditate da AppleDB
    specs = {
        "Architettura": "64-bit ARM" if ("A" in chip or "M" in chip) else "32-bit ARM" if "AP" in chip else "32-bit / Intel",
        "Processore / SoC": chip
    }
    
    name_lower = name.lower()
    
    # --- ARCHIVIO STORICO COMMERCIALE IPHONE ---
    if "iphone" in name_lower:
        specs["Sistema Operativo"] = "iOS"
        
        # Serie iPhone 16
        if "iphone 16 pro" in name_lower:
            specs["Display"] = "Super Retina XDR OLED ProMotion 120Hz (6.3\" o 6.9\")"
            specs["Fotocamera"] = "Fusiòne 48MP | Ultra-grandangolo 48MP | Teleobiettivo 5x 12MP"
            specs["Materiale"] = "Titanio Grado 5 con finitura satinata"
            specs["Connettore"] = "USB-C (USB 3 fino a 10Gb/s)"
            specs["Sicurezza"] = "Face ID & Controllo Fotocamera"
        elif "iphone 16" in name_lower:
            specs["Display"] = "Super Retina XDR OLED con Dynamic Island (6.1\" o 6.7\")"
            specs["Fotocamera"] = "Principale 48MP | Ultra-grandangolo 12MP"
            specs["Connettore"] = "USB-C (USB 2)"
            specs["Sicurezza"] = "Face ID & Tasto Azione"

        # Serie iPhone 15
        elif "iphone 15 pro" in name_lower:
            specs["Display"] = "Super Retina XDR OLED ProMotion 120Hz (6.1\" o 6.7\")"
            specs["Fotocamera"] = "Principale 48MP | Ultra-grandangolo 12MP | Tele 3x/5x 12MP"
            specs["Materiale"] = "Titanio Aero-spaziale"
            specs["Connettore"] = "USB-C (USB 3)"
            specs["Sicurezza"] = "Face ID"
        elif "iphone 15" in name_lower:
            specs["Display"] = "Super Retina XDR OLED con Dynamic Island (6.1\" o 6.7\")"
            specs["Fotocamera"] = "Principale 48MP | Ultra-grandangolo 12MP"
            specs["Connettore"] = "USB-C (USB 2)"
            specs["Sicurezza"] = "Face ID"

        # Serie iPhone 14
        elif "iphone 14 pro" in name_lower:
            specs["Display"] = "Super Retina XDR OLED Always-On con Dynamic Island"
            specs["Fotocamera"] = "Principale 48MP | Ultra-grandangolo 12MP | Tele 3x 12MP"
            specs["Connettore"] = "Lightning"
            specs["Sicurezza"] = "Face ID & Rilevamento Incidenti"
        elif "iphone 14" in name_lower:
            specs["Display"] = "Super Retina XDR OLED (6.1\" o 6.7\")"
            specs["Fotocamera"] = "Doppia Fotocamera 12MP con Photonic Engine"
            specs["Connettore"] = "Lightning"
            specs["Sicurezza"] = "Face ID"

        # Serie iPhone 13 / 12
        elif "iphone 13" in name_lower or "iphone 12" in name_lower:
            specs["Display"] = "Super Retina XDR OLED"
            specs["Fotocamera"] = "Doppia Fotocamera 12MP (Grandangolo e Ultra-grandangolo)"
            specs["Connettore"] = "Lightning"
            specs["Sicurezza"] = "Face ID"

        # Serie iPhone 11 / XR
        elif "iphone 11" in name_lower or "iphone xr" in name_lower:
            specs["Display"] = "Liquid Retina HD IPS"
            specs["Fotocamera"] = "Doppia 12MP (11) / Singola 12MP (XR)"
            specs["Connettore"] = "Lightning"
            specs["Sicurezza"] = "Face ID"

        # Storici (iPhone X, 8, 7, 6, 5, 4, 3G, 2G)
        elif "iphone x" in name_lower:
            specs["Display"] = "Super Retina OLED da 5.8 pollici (Primo OLED)"
            specs["Fotocamera"] = "Doppia 12MP con doppia stabilizzazione ottica"
            specs["Sicurezza"] = "Face ID (Introdotto con questo modello)"
            specs["Connettore"] = "Lightning"
        elif "iphone 7" in name_lower or "iphone 8" in name_lower:
            specs["Display"] = "Retina HD Display con 3D Touch"
            specs["Fotocamera"] = "12MP (Grandangolo singolo o doppio su Plus)"
            specs["Sicurezza"] = "Touch ID capacitivo con Tasto Home a stato solido"
        elif "iphone 6" in name_lower:
            specs["Display"] = "Retina HD Display (Primo aumento di schermo a 4.7\" e 5.5\")"
            specs["Fotocamera"] = "8MP iSight con Focus Pixels"
            specs["Sicurezza"] = "Touch ID"
        elif "iphone 5" in name_lower:
            specs["Display"] = "Retina Display da 4 pollici (Formato 16:9)"
            specs["Connettore"] = "Lightning (Introdotto con questo modello)"
            specs["Rete"] = "Primo iPhone con supporto 4G LTE"
        elif "iphone 4" in name_lower:
            specs["Display"] = "Retina Display (960x640 - Massima densità dell'epoca)"
            specs["Design"] = "Vetro anteriore/posteriore e banda laterale in acciaio"
            specs["Fotocamera"] = "5MP con Flash LED & Registrazione HD 720p"
        elif "iphone 3g" in name_lower:
            specs["Display"] = "3.5 pollici LCD Touchscreen (320x480)"
            specs["Rete"] = "Supporto reti 3G UMTS & GPS Integrato"
            specs["Scocca"] = "Plastica lucida nera o bianca"
        elif "iphone (original)" in name_lower or "1st generation" in name_lower or key == "iPhone1,1":
            specs["Display"] = "3.5 pollici Multi-Touch (320x480 a 163 ppi)"
            specs["Fotocamera"] = "2.0 Megapixel (Niente Flash, Niente Video)"
            specs["Rete"] = "2G GSM / EDGE (Quad-band)"
            specs["Storage"] = "4GB, 8GB o 16GB"
            specs["Nota Storica"] = "Il primo iPhone della storia presentato da Steve Jobs."

    # --- ARCHIVIO MAC ---
    elif "mac" in name_lower:
        specs["Sistema Operativo"] = "macOS"
        if "air" in name_lower:
            specs["Display"] = "Liquid Retina Display con True Tone"
            specs["Design"] = "Architettura Fanless ultra-sottile priva di ventole"
        elif "pro" in name_lower:
            specs["Display"] = "Liquid Retina XDR con tecnologia Mini-LED e ProMotion"
            specs["Audio"] = "Sistema a sei altoparlanti Hi-Fi con woofer force-cancelling"
        else:
            specs["Display"] = "Retina 4.5K / 5K" if "imac" in name_lower else "Uscita Video Thunderbolt"

    # --- ARCHIVIO IPAD ---
    elif "ipad" in name_lower:
        specs["Sistema Operativo"] = "iPadOS"
        if "pro" in name_lower and "m4" in chip:
            specs["Display"] = "Ultra Retina XDR (Tandem OLED a doppio strato)"
            specs["Spessore"] = "5.1 mm (Il prodotto Apple più sottile di sempre)"
        elif "pro" in name_lower:
            specs["Display"] = "Liquid Retina XDR (Mini-LED) con ProMotion"
        else:
            specs["Display"] = "Liquid Retina Display"

    # Pulizia finale dei campi vuoti
    return {k: v for k, v in specs.items() if v and v != "N/A" and v != ""}

def build_apple_database():
    print("📡 Download dell'intero catalogo da AppleDB...")
    url = "https://api.appledb.dev/device/main.json"
    response = requests.get(url)
    data = response.json()
    
    raw_list = data if isinstance(data, list) else list(data.values())
    apple_devices = []
    
    for item in raw_list:
        name = item.get("name", "")
        device_type = item.get("type", "")
        key = item.get("key", "")
        
        # Filtro selettivo categorie reali ed eliminazione modelli beta o prototipi
        if device_type not in ["Mac", "iPhone", "iPad", "Watch"]:
            continue
        if any(bad_word in name.lower() for bad_word in ["beta", "unreleased", "simulator", "developer", "unknown", "internal"]):
            continue
            
        released = item.get("released", [""])
        release_date = released[0] if isinstance(released, list) and len(released) > 0 else (released if isinstance(released, str) else "")
        year = release_date[:4] if len(release_date) >= 4 else "N/A"
        
        if year == "N/A":
            continue
            
        chip = str(item.get("soc", "Apple / Intel / Motorola"))
        category = device_type
        
        # Colori identificativi dell'ecosistema per l'effetto Liquid Glass
        theme_color = "#8A8B8C" if "iPhone" in name else ("#007AFF" if "Mac" in name else "#FF2D55")
        
        # Recupero identificativo di sistema per l'assegnazione delle immagini ufficiali
        identifier = item.get("identifier", [])
        ident_list = identifier if isinstance(identifier, list) else [identifier]
        
        first_ident = ident_list[0] if ident_list else key
        image_key = urllib.parse.quote(str(first_ident))
        image_url = f"https://img.appledb.dev/device@256/{image_key}/0.png"
        
        # Generazione e iniezione delle schede commerciali Mactracker
        board = item.get("board", [])
        board_str = ", ".join(board) if isinstance(board, list) else str(board)
        model = item.get("model", [])
        model_str = ", ".join(model) if isinstance(model, list) else str(model)
        
        specs = get_commercial_specs(name, key, chip, year)
        specs["Data di Lancio"] = release_date
        specs["Model Identifier"] = ", ".join(ident_list)
        
        apple_devices.append({
            "id": key,
            "name": name,
            "chip": chip if chip != "N/A" else "Nativo",
            "releaseYear": year,
            "category": category,
            "imageURL": image_url,
            "themeColor": theme_color,
            "specs": specs
        })
        
    # Ordinamento cronologico decrescente (dai più nuovi ai più storici)
    apple_devices.sort(key=lambda x: str(x["releaseYear"]), reverse=True)
    
    with open("apple_database.json", "w", encoding="utf-8") as f:
        json.dump(apple_devices, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Compilazione completata con successo! Inseriti {len(apple_devices)} dispositivi reali.")

if __name__ == "__main__":
    build_apple_database()
