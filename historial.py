# historial.py
import json
import os

HISTORIAL_FILE = "historial.json"

def guardar_en_historial(data, algoritmo):
    historial = cargar_historial()
    historial.append({"algoritmo": algoritmo, "data": data})
    with open(HISTORIAL_FILE, "w") as f:
        json.dump(historial, f)

def cargar_historial():
    if not os.path.exists(HISTORIAL_FILE):
        return []
    with open(HISTORIAL_FILE, "r") as f:
        return json.load(f)
