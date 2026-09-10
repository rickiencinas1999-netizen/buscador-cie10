# -*- coding: utf-8 -*-
"""
Arma webapp/index.html a partir de src/plantilla_app.html + dist/app_data.json,
incrustando los datos directamente en el HTML para que la app sea un solo
archivo autocontenido (sin llamadas de red, sirve para GitHub Pages o abrir
localmente con doble clic).

Requiere haber corrido antes generar_datos_app.py.

Este script solo (re)genera webapp/index.html. Los demás archivos de
webapp/ (manifest.json, sw.js, icon-192.png, icon-512.png) son estáticos,
no se regeneran, y no hace falta tocarlos salvo que se quiera cambiar el
ícono o el nombre de la app instalada.

Uso:
    python3 generar_datos_app.py
    python3 construir_app.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA_PATH = ROOT / "dist" / "app_data.json"
TEMPLATE_PATH = HERE / "plantilla_app.html"
OUT_PATH = ROOT / "webapp" / "index.html"

with open(DATA_PATH, encoding="utf-8") as f:
    data_str = f.read()
data = json.loads(data_str)
total_codes = len(data["codes"])
total_tagged = len(data["tags"])

tpl = TEMPLATE_PATH.read_text(encoding="utf-8")
out = tpl.replace("__DATA_JSON__", data_str)
out = out.replace("__TOTAL_CODES__", str(total_codes))
out = out.replace("__TOTAL_TAGGED__", str(total_tagged))

OUT_PATH.parent.mkdir(exist_ok=True)
OUT_PATH.write_text(out, encoding="utf-8")
print("escrito:", OUT_PATH, "-", len(out.encode("utf-8")), "bytes")
