# -*- coding: utf-8 -*-
"""
Arma webapp/index.html a partir de src/plantilla_app.html + dist/app_data.json,
incrustando los datos directamente en el HTML para que la app sea un solo
archivo autocontenido (sin llamadas de red, sirve para GitHub Pages, Render
o abrir localmente con doble clic).

Requiere haber corrido antes generar_datos_app.py.

Este script también espeja todo a docs/, con el mismo contenido que
webapp/ (index.html + manifest.json + sw.js + íconos). Eso es porque
GitHub Pages, cuando se configura como "Deploy from a branch", solo puede
publicar la raíz del repo o una carpeta llamada exactamente "docs" — no
"webapp". Con docs/ ya listo, GitHub Pages funciona sin depender de
GitHub Actions (evita problemas de permisos/verificación de cuenta).

Uso:
    python3 generar_datos_app.py
    python3 construir_app.py
"""
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA_PATH = ROOT / "dist" / "app_data.json"
TEMPLATE_PATH = HERE / "plantilla_app.html"
OUT_PATH = ROOT / "webapp" / "index.html"
DOCS_DIR = ROOT / "docs"
STATIC_ASSETS = ("manifest.json", "sw.js", "icon-192.png", "icon-512.png", "hospital-logo.png")

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

# espejo en docs/ para GitHub Pages ("Deploy from a branch" -> /docs)
DOCS_DIR.mkdir(exist_ok=True)
(DOCS_DIR / "index.html").write_text(out, encoding="utf-8")
for name in STATIC_ASSETS:
    src = ROOT / "webapp" / name
    if src.exists():
        shutil.copyfile(src, DOCS_DIR / name)
print("espejo escrito en:", DOCS_DIR)
