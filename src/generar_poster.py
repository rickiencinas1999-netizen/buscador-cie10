# -*- coding: utf-8 -*-
"""
Genera dist/poster.html: el póster imprimible (tamaño carta horizontal, una
portada + una o más páginas por especialidad) a partir de especialidades.py.

Para convertirlo a PDF hace falta un navegador headless (Chromium vía
Playwright, por ejemplo) — este script solo produce el HTML listo para
imprimir o convertir.

Uso:
    python3 generar_poster.py
"""
import json, html, colorsys, datetime, math
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CATALOGO_PATH = ROOT / "data" / "catalogo.json"
OUT_PATH = ROOT / "dist" / "poster.html"

with open(CATALOGO_PATH, encoding='utf-8') as f:
    CAT = json.load(f)

spec = importlib.util.spec_from_file_location("especialidades", HERE / "especialidades.py")
bd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bd)
SPECIALTIES = bd.SPECIALTIES

ORDER = list(SPECIALTIES.keys())
N = len(ORDER)
COLORS = {}
for i, s in enumerate(ORDER):
    h = i / N
    r, g, b = colorsys.hls_to_rgb(h, 0.36, 0.62)
    COLORS[s] = '#%02X%02X%02X' % (int(r*255), int(g*255), int(b*255))

def esc(t):
    return html.escape(t)

def titlecase_dx(name):
    keep_upper = {"VIH","COVID-19","EPOC","ADN","ARN","IRA","IVU","TB","IAM","EPI","DIU","SIRS"}
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
    res = ' '.join(out)
    return res

TOTAL_CODES = sum(len(codes) for cats in SPECIALTIES.values() for _, codes in cats)
SPEC_TOTAL = {s: sum(len(codes) for _, codes in cats) for s, cats in SPECIALTIES.items()}
SUBCAT_COUNT = {s: len(v) for s, v in SPECIALTIES.items()}

today = datetime.date.today()
fecha_str = today.strftime('%d/%m/%Y')

MAX_PER_PAGE = 40

def paginate_subcats(cats, max_per_page=MAX_PER_PAGE):
    total = sum(len(codes) for _, codes in cats)
    if total <= max_per_page:
        return [cats]
    num_pages = math.ceil(total / max_per_page)
    target = math.ceil(total / num_pages)
    pages, current, current_n = [], [], 0
    for subcat, codes in cats:
        if current and current_n + len(codes) > target and len(pages) < num_pages - 1:
            pages.append(current)
            current, current_n = [], 0
        current.append((subcat, codes))
        current_n += len(codes)
    if current:
        pages.append(current)
    return pages

# Precompute all page chunks per specialty
SPEC_CHUNKS = {s: paginate_subcats(cats) for s, cats in SPECIALTIES.items()}
TOTAL_PAGES = 1 + sum(len(chunks) for chunks in SPEC_CHUNKS.values())

CSS = """
@page { size: 11in 8.5in; margin: 0; }
* { box-sizing: border-box; }
html, body { margin:0; padding:0; }
body {
  font-family: Arial, Helvetica, sans-serif;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
  color: #1a1a1a;
}
.page {
  width: 11in;
  height: 8.5in;
  position: relative;
  page-break-after: always;
  overflow: hidden;
  padding: 0.35in 0.5in 0.32in 0.5in;
  display: flex;
  flex-direction: column;
}
.page:last-child { page-break-after: avoid; }

/* ===== Cover ===== */
.cover { justify-content: center; align-items: flex-start; }
.cover-kicker {
  font-size: 13px; letter-spacing: 3px; font-weight: 700; color: #555;
  text-transform: uppercase; margin-bottom: 10px;
}
.cover h1 {
  font-size: 46px; margin: 0 0 6px 0; color: #16202A; line-height:1.08;
}
.cover .sub {
  font-size: 17px; color: #3a3a3a; margin-bottom: 26px; max-width: 8.6in; line-height:1.45;
}
.cover-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px 18px; width: 100%; margin-top: 6px;
}
.cover-item {
  display: flex; align-items: center; gap: 10px;
  border-left: 7px solid var(--c);
  background: #F7F7F7;
  padding: 9px 12px;
  border-radius: 4px;
}
.cover-item .num {
  font-weight: 800; font-size: 13px; color: #fff; background: var(--c);
  width: 24px; height: 24px; border-radius: 50%; display:flex; align-items:center; justify-content:center; flex: 0 0 auto;
}
.cover-item .name { font-size: 14.5px; font-weight: 700; color: #16202A; }
.cover-item .cnt { font-size: 11px; color: #666; font-weight: 500; }
.cover-foot {
  position: absolute; bottom: 0.3in; left: 0.5in; right: 0.5in;
  font-size: 10.5px; color: #777; border-top: 1px solid #ddd; padding-top: 8px;
  display:flex; justify-content: space-between;
}

/* ===== Specialty page ===== */
.head {
  display: flex; align-items: center; justify-content: space-between;
  border-bottom: 6px solid var(--c);
  padding-bottom: 10px; margin-bottom: 12px; flex: 0 0 auto;
}
.head-left { display:flex; align-items:baseline; gap: 14px; }
.head h1 { font-size: 28px; margin: 0; color: #16202A; }
.head .part { font-size: 16px; color: #888; font-weight: 600; margin-left: 8px; }
.head .kicker { font-size: 11.5px; letter-spacing: 2px; text-transform: uppercase; color: var(--c); font-weight: 800; }
.head .count-badge {
  background: var(--c); color:#fff; font-weight:800; font-size: 13px;
  padding: 7px 14px; border-radius: 20px; white-space:nowrap;
}
.body-cols {
  column-gap: 0.34in; flex: 1 1 auto; overflow: hidden;
}
.body-cols.cols-3 { columns: 3; }
.body-cols.cols-2 { columns: 2; }
.subcat {
  break-inside: avoid; -webkit-column-break-inside: avoid;
  margin-bottom: 11px; display: inline-block; width: 100%;
}
.subcat h2 {
  font-size: 12.5px; text-transform: uppercase; letter-spacing: 0.6px;
  color: #fff; background: var(--c); display:inline-block;
  padding: 3px 9px; border-radius: 3px; margin: 0 0 6px 0; font-weight: 700;
}
.dx { display:flex; align-items: flex-start; gap: 8px; padding: 3.2px 0; border-bottom: 1px solid #ececec; }
.dx .code {
  font-family: 'Consolas','Courier New',monospace; font-weight: 800; font-size: 12px;
  color: var(--c); background: color-mix(in srgb, var(--c) 12%, white);
  border: 1.3px solid var(--c); border-radius: 4px; padding: 1px 6px; flex: 0 0 auto; min-width: 44px; text-align:center;
}
.dx .nm { font-size: 11.5px; line-height: 1.25; color: #1c1c1c; padding-top: 1px; }
.notes {
  flex: 0 0 auto; margin-top: 6px; padding: 8px 14px; border: 1.4px dashed #c9c9c9; border-radius: 5px;
  display:flex; gap: 16px; background: #FBFBFB;
}
.notes .lbl { font-size: 10px; color: #999; font-weight: 700; text-transform: uppercase; letter-spacing: .4px; flex: 0 0 auto; padding-top:2px; }
.notes .lines { flex: 1 1 auto; display:flex; flex-direction:column; gap: 12px; padding-top: 3px; }
.notes .lines div { border-bottom: 1px solid #d8d8d8; height: 1px; }
.foot {
  flex: 0 0 auto; margin-top: 8px; padding-top: 7px; border-top: 1px solid #ddd;
  display:flex; justify-content: space-between; font-size: 10px; color: #888;
}
"""

def cover_page():
    items = []
    for i, spec_name in enumerate(ORDER, start=1):
        c = COLORS[spec_name]
        cnt = SUBCAT_COUNT[spec_name]
        codes_n = SPEC_TOTAL[spec_name]
        items.append(f"""
        <div class="cover-item" style="--c:{c}">
          <div class="num">{i}</div>
          <div>
            <div class="name">{esc(spec_name)}</div>
            <div class="cnt">{codes_n} códigos &middot; {cnt} categorías</div>
          </div>
        </div>""")
    return f"""
    <div class="page cover">
      <div class="cover-kicker">Guía rápida de codificación &middot; Archivo Clínico / Estadística</div>
      <h1>Diagnósticos CIE-10 por especialidad</h1>
      <div class="sub">Selección amplia de códigos CIE-10 (edición vigente, actualización abril 2024) organizada por
      especialidad y agrupada por categoría clínica, incluyendo diagnósticos relacionados además de los más
      frecuentes, para consulta rápida en el punto de captura. Recorta o separa la hoja de cada especialidad y
      colócala en el pizarrón frente a la computadora del área correspondiente.</div>
      <div class="cover-grid">
        {''.join(items)}
      </div>
      <div class="cover-foot">
        <span>Fuente: Catálogo CIE-10 institucional (CIE-ABRIL-2024) &middot; {TOTAL_CODES} códigos incluidos en esta guía</span>
        <span>Elaborado {fecha_str} &middot; Ante duda diagnóstica, consultar el catálogo completo con Archivo Clínico</span>
      </div>
    </div>
    """

def specialty_page(spec_name, chunk, part_idx, part_total, page_idx):
    c = COLORS[spec_name]
    codes_n = sum(len(codes) for _, codes in chunk)
    subcats_html = []
    for subcat, codes in chunk:
        rows = []
        for code in codes:
            nombre = CAT[code]['nombre']
            display_code = code[:-1] if code.endswith('X') and len(code) == 4 else code
            rows.append(f"""<div class="dx"><div class="code">{esc(display_code)}</div><div class="nm">{esc(titlecase_dx(nombre))}</div></div>""")
        subcats_html.append(f"""
        <div class="subcat">
          <h2>{esc(subcat)}</h2>
          {''.join(rows)}
        </div>""")
    colcls = "cols-3" if codes_n >= 24 else "cols-2"
    part_label = f'<span class="part">({part_idx}/{part_total})</span>' if part_total > 1 else ""
    total_badge = f"{SPEC_TOTAL[spec_name]} códigos" if part_total == 1 else f"{codes_n} de {SPEC_TOTAL[spec_name]} códigos"
    return f"""
    <div class="page" style="--c:{c}">
      <div class="head">
        <div class="head-left">
          <div>
            <div class="kicker">Diagnósticos CIE-10 por especialidad</div>
            <h1>{esc(spec_name)}{part_label}</h1>
          </div>
        </div>
        <div class="count-badge">{total_badge}</div>
      </div>
      <div class="body-cols {colcls}">
        {''.join(subcats_html)}
      </div>
      <div class="notes">
        <div class="lbl">Espacio para&nbsp;anotar<br>otros códigos&nbsp;de tu&nbsp;área</div>
        <div class="lines">{'<div></div>' * 2}</div>
      </div>
      <div class="foot">
        <span>Guía práctica de codificación &middot; {esc(spec_name)} &middot; pág. {page_idx} de {TOTAL_PAGES}</span>
        <span>Diagnóstico complejo o no listado: consultar catálogo completo CIE-10 con Archivo Clínico / Estadística</span>
      </div>
    </div>
    """

pages = [cover_page()]
page_idx = 2
for spec_name in ORDER:
    chunks = SPEC_CHUNKS[spec_name]
    part_total = len(chunks)
    for part_idx, chunk in enumerate(chunks, start=1):
        pages.append(specialty_page(spec_name, chunk, part_idx, part_total, page_idx))
        page_idx += 1

doc = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>CIE-10 por especialidad</title>
<style>{CSS}</style>
</head>
<body>
{''.join(pages)}
</body>
</html>"""

OUT_PATH.parent.mkdir(exist_ok=True)
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(doc)

print("HTML generado:", len(pages), "páginas ->", OUT_PATH)
print("Para PDF: abre ese HTML con un navegador headless e imprime a PDF")
print("tamaño carta horizontal (11in x 8.5in), sin márgenes.")
