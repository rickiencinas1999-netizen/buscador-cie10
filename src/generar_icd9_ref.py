# -*- coding: utf-8 -*-
"""
Genera data/icd9_3digit_ref.json: lista oficial de categorías de 3 dígitos
de la CIE-9-MC (ICD-9-CM), código -> nombre en inglés.

Fuente: "Appendix E - List of Three-Digit Categories" del manual oficial de
la CIE-9-MC de EE. UU., edición FY2012 (CDC/NCHS), archivo
DC_3D12.RTF, guardado en data/cdc_icd9cm_source/ (el .zip original de la
CDC, Appndx12.zip, también se conserva ahí para trazabilidad).

Este archivo NO es una tabla de equivalencia CIE-9<->CIE-10 (esa no existe
gratis para la edición CIE-10 que usa este catálogo — ver el comentario en
cie9_correlacion.py). Es solo el catálogo oficial de códigos y nombres de
la CIE-9-MC, y se usa como referencia para verificar que cada código que
aparece en cie9_correlacion.py exista de verdad y tenga el nombre que se le
atribuye — así una correlación curada a mano no incluye números de código
inventados o mal recordados.

Uso:
    python3 generar_icd9_ref.py
"""
import re
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RTF_PATH = ROOT / "data" / "cdc_icd9cm_source" / "DC_3D12.RTF"
OUT_PATH = ROOT / "data" / "icd9_3digit_ref.json"

# Extractor de texto de RTF deliberadamente simple: no interpreta el RTF de
# verdad (tablas de fuentes, estilos, etc.), solo tira las palabras de
# control y llaves para quedarse con el texto plano. Es suficiente para este
# documento porque es texto corrido sin tablas ni formato complejo.
def rtf_to_text(path):
    with open(path, encoding="cp1252", errors="ignore") as f:
        data = f.read()
    text = re.sub(r"\\par[d]?\b", "\n", data)
    text = re.sub(r"\\[a-zA-Z]+-?\d* ?", "", text)
    text = re.sub(r"[{}]", "", text)
    text = text.replace("\\\\", "")
    return text


# líneas como " 001Cholera", " 042 Human immunodeficiency virus...", "V01...", "E800..."
LINE_RE = re.compile(r"^\s*((?:\d{3}|V\d{2}|E\d{3})(?:\.\d+)?)\s*([A-Z][^\n]*)$", re.MULTILINE)


def build_reference():
    text = rtf_to_text(RTF_PATH)
    out = {}
    for code, name in LINE_RE.findall(text):
        out[code] = name.strip()
    return out


if __name__ == "__main__":
    ref = build_reference()
    print("categorías extraídas:", len(ref))
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(ref, f, ensure_ascii=False, indent=1, sort_keys=True)
    print("escrito en:", OUT_PATH)
