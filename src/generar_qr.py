# -*- coding: utf-8 -*-
"""
Genera un código QR (PNG) que apunta a la URL donde quedó publicada la app
(GitHub Pages o Render), para imprimir y pegar junto al póster en el
pizarrón: cualquiera lo escanea con el teléfono y abre el buscador.

Requiere el paquete "qrcode":
    pip install qrcode[pil]

Uso:
    python3 generar_qr.py https://tu-usuario.github.io/buscador-cie10/
    python3 generar_qr.py https://buscador-cie10.onrender.com

El PNG se guarda en dist/qr.png.
"""
import sys
from pathlib import Path

try:
    import qrcode
except ImportError:
    sys.exit("Falta el paquete 'qrcode'. Instálalo con: pip install qrcode[pil]")

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "dist" / "qr.png"

if len(sys.argv) != 2:
    sys.exit("Uso: python3 generar_qr.py <URL de la app publicada>")

url = sys.argv[1]

img = qrcode.make(url, box_size=12, border=3)
OUT_PATH.parent.mkdir(exist_ok=True)
img.save(OUT_PATH)
print("QR listo:", OUT_PATH, "->", url)
