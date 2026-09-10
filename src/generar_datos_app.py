# -*- coding: utf-8 -*-
"""
Genera dist/app_data.json: el bundle de datos que consume la app web
(webapp/index.html) — el catálogo CIE-10 completo (código + nombre) más las
etiquetas de especialidad/categoría tomadas de especialidades.py.

Uso:
    python3 generar_datos_app.py
"""
import json
import colorsys
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CATALOGO_PATH = ROOT / "data" / "catalogo.json"
OUT_PATH = ROOT / "dist" / "app_data.json"

with open(CATALOGO_PATH, encoding="utf-8") as f:
    CAT = json.load(f)

spec = importlib.util.spec_from_file_location("especialidades", HERE / "especialidades.py")
bd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bd)
SPECIALTIES = bd.SPECIALTIES

spec2 = importlib.util.spec_from_file_location("sinonimos", HERE / "sinonimos.py")
sy = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(sy)
SYNONYMS = sy.SYNONYMS

ORDER = list(SPECIALTIES.keys())
N = len(ORDER)
COLORS = {}
for i, s in enumerate(ORDER):
    h = i / N
    r, g, b = colorsys.hls_to_rgb(h, 0.36, 0.62)
    COLORS[s] = '#%02X%02X%02X' % (int(r * 255), int(g * 255), int(b * 255))


def titlecase_dx(name):
    keep_upper = {"VIH", "COVID-19", "EPOC", "ADN", "ARN", "IRA", "IVU", "TB", "IAM", "EPI", "DIU", "SIRS"}
    words = name.split(' ')
    out = []
    for i, w in enumerate(words):
        raw = w.strip('()[],.')
        core = raw
        if core.upper() in keep_upper:
            out.append(w)
            continue
        if core.isdigit():
            out.append(w)
            continue
        lw = w.lower()
        if i == 0:
            lw = lw[0].upper() + lw[1:] if lw else lw
        out.append(lw)
    return ' '.join(out)


# Catálogo completo: códigos + nombres ordenados (título-caso para mostrar)
# se descartan renglones basura/centinela (p. ej. código "9999" con nombre no-texto)
codes_sorted = sorted(c for c, v in CAT.items() if isinstance(v['nombre'], str) and v['nombre'].strip())
names_sorted = [titlecase_dx(CAT[c]['nombre']) for c in codes_sorted]

# Etiquetas curadas: código -> lista de [indice_especialidad, categoria]
tags = {}
for spec_idx, spec_name in enumerate(ORDER):
    for subcat, codes in SPECIALTIES[spec_name]:
        for code in codes:
            tags.setdefault(code, []).append([spec_idx, subcat])

specialties_meta = [{"name": s, "color": COLORS[s]} for s in ORDER]

# valida que cada código de un sinónimo exista en el catálogo completo
valid_codes = set(codes_sorted)
synonyms_out = {}
for term, codes in SYNONYMS.items():
    good = [c for c in codes if c in valid_codes]
    if good:
        synonyms_out[term] = good

out = {
    "codes": codes_sorted,
    "names": names_sorted,
    "tags": tags,
    "specialties": specialties_meta,
    "synonyms": synonyms_out,
}

s = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
OUT_PATH.parent.mkdir(exist_ok=True)
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(s)

print("bytes:", len(s.encode('utf-8')))
print("codes:", len(codes_sorted), "tagged:", len(tags), "sinonimos:", len(synonyms_out))
print("escrito en:", OUT_PATH)
