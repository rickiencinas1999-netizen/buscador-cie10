# -*- coding: utf-8 -*-
"""
Genera data/cie10_a_cie11.json: correlación CIE-10 -> CIE-11, código por
código, para cada código de data/catalogo.json que tenga equivalente.

Fuente: tabla oficial de la OMS "10To11MapToOneCategory" (descargada desde
el navegador de la CIE-11, icd.who.int/browse — pestaña "Info" -> "ICD-10 /
ICD-11 mapping Tables"), versión 2025-Jan-24, guardada en
data/oms_cie11_source/10To11MapToOneCategory.txt. Es la tabla "a una sola
categoría": cuando un código de la CIE-10 corresponde a más de un código de
la CIE-11 (existe también "10To11MapToMultipleCategories"), la OMS ya eligió
aquí la mejor correspondencia única.

Los códigos de la OMS vienen con punto decimal (p. ej. "I21.9") y a veces
sin subdivisión (p. ej. "T68"); el catálogo institucional que usa esta app
no lleva punto y rellena la subdivisión que falta con "X" (p. ej. "I219",
"T68X"). normalize_variants() cubre esa diferencia de formato.

Un puñado de códigos curados (menos del 2%) no tienen una fila que calce
por diferencias de fondo entre la edición de la OMS de este archivo y la
edición mexicana del catálogo (p. ej. la OMS reclasificó del todo la
diabetes/dengue/enfermedad renal crónica en años recientes). Para esos se
usa MANUAL_OVERRIDES: la fila de la OMS clínicamente más cercana, elegida
a mano y documentada aquí, en vez de dejarlos sin CIE-11.

Uso:
    python3 generar_cie11.py
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CATALOGO_PATH = ROOT / "data" / "catalogo.json"
WHO_MAP_PATH = ROOT / "data" / "oms_cie11_source" / "10To11MapToOneCategory.txt"
OUT_PATH = ROOT / "data" / "cie10_a_cie11.json"

with open(CATALOGO_PATH, encoding="utf-8") as f:
    CAT_CODES = set(json.load(f).keys())

# código de catálogo (sin punto, con "X" de relleno) -> código de la OMS tal
# como aparece en el archivo fuente (con punto). Elegido a mano revisando el
# bloque completo de la CIE-10 de la OMS para el diagnóstico en cuestión.
MANUAL_OVERRIDES = {
    "A90X": "A97.9",  # Fiebre del dengue [clásico] -> OMS reclasificó dengue bajo A97; A97.9 = "Dengue, no especificado"
    "N180": "N18.5",  # Insuficiencia renal terminal -> OMS ahora estadifica ERC; etapa 5 = terminal
    "K589": "K58",    # Colon irritable sin diarrea -> no hay subdivisión "sin diarrea" en la OMS; usa la categoría genérica
    "K359": "K35.8",  # Apendicitis aguda, no especificada -> "Acute appendicitis, other and unspecified"
    "X499": "X49",    # Envenenamiento accidental..., lugar no especificado -> la OMS no subdivide por lugar
}


def normalize_variants(who_code):
    """Variantes del código de catálogo que podrían corresponder a este
    código de la OMS (que trae punto y a veces no tiene 4to carácter)."""
    no_dot = who_code.replace(".", "")
    variants = {no_dot}
    if len(no_dot) == 3:
        variants.add(no_dot + "X")
    return variants


def load_who_rows():
    with open(WHO_MAP_PATH, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def build_mapping():
    rows = load_who_rows()
    by_who_code = {}
    for row in rows:
        code = row.get("icd10Code")
        if code:
            by_who_code[code] = row

    mapping = {}
    for row in rows:
        who_code = row.get("icd10Code")
        if not who_code:
            continue
        icd11_code = row.get("icd11Code")
        if not icd11_code:
            continue
        entry = {"code": icd11_code, "title": row.get("icd11Title", "")}
        for variant in normalize_variants(who_code):
            if variant in CAT_CODES and variant not in mapping:
                mapping[variant] = entry

    overrides_applied = []
    overrides_missing = []
    for cat_code, who_code in MANUAL_OVERRIDES.items():
        if cat_code not in CAT_CODES:
            continue
        row = by_who_code.get(who_code)
        if not row or not row.get("icd11Code"):
            overrides_missing.append((cat_code, who_code))
            continue
        mapping[cat_code] = {"code": row["icd11Code"], "title": row.get("icd11Title", "")}
        overrides_applied.append(cat_code)

    return mapping, overrides_applied, overrides_missing


if __name__ == "__main__":
    mapping, overrides_applied, overrides_missing = build_mapping()
    print("códigos del catálogo con equivalente CIE-11:", len(mapping), "/", len(CAT_CODES))
    print("overrides manuales aplicados:", overrides_applied)
    if overrides_missing:
        print("OVERRIDES SIN RESOLVER (revisar MANUAL_OVERRIDES):", overrides_missing)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    print("escrito en:", OUT_PATH)
