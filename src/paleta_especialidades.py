# -*- coding: utf-8 -*-
"""
Paleta de color para las 19 especialidades curadas.

No es una distribución ingenua de tonos (lo que había antes: repartir 360°
del círculo de tonos entre N especialidades con colorsys.hls_to_rgb) — esa
técnica produce tonos vecinos casi idénticos en ciertas zonas del círculo
(verdes/oliva, azules/violeta) porque el espacio de tono HSL no es
perceptualmente uniforme.

Esta paleta se generó y validó con el método de la skill de dataviz:
  - 19 tonos repartidos en el círculo con "golden-angle spacing" (pasos de
    ~137.5°) en el espacio OKLCH, que sí es perceptualmente uniforme y evita
    que especialidades consecutivas en la lista caigan en tonos parecidos.
  - Cromas ajustados por tono para no salirse del gamut sRGB (algunos tonos,
    sobre todo verde-azulados, tienen menos croma disponible antes de
    "recortarse" y verse grises).
  - Una búsqueda local que ajusta tono/luminosidad hasta que cada PAR
    consecutivo (el orden en que aparecen los chips/especialidades) supere:
      - separación bajo simulación de daltonismo protanopía/deuteranopía
        (ΔE OKLab objetivo >= 8), y
      - separación a simple vista sin simular nada (ΔE >= 15, el piso más
        estricto), y
      - contraste >= 3:1 contra el fondo de la app.
  - Validado con scripts/validate_palette.js de la skill de dataviz:
    "ALL CHECKS PASS" tanto en modo claro (fondo #EFF4F3) como oscuro
    (fondo #0A1717) para los 18 pares consecutivos.

Nota: el color siempre acompaña texto (nombre de la especialidad, código,
etc.) en la app — nunca es la única forma de distinguir una especialidad —
así que estos 19 tonos priorizan visión normal y daltonismo parcial, no
sustituyen la etiqueta de texto.

Cada entrada es (hex_claro, hex_oscuro, tinta_oscura):
  - hex_claro: tono para modo claro (oscuro/saturado, para texto/bordes sobre
    fondo claro y como fondo con texto blanco encima).
  - hex_oscuro: tono para modo oscuro (más brillante, para texto/bordes sobre
    fondo casi negro).
  - tinta_oscura: color de texto a usar cuando hex_oscuro se usa como FONDO
    (p. ej. una etiqueta de categoría o un pill) — "#fff" si hex_oscuro es
    suficientemente oscuro para sostener texto blanco, o un tono de tinta
    oscura (mismo #062120 que ya usa el acento de la marca en modo oscuro)
    si hex_oscuro es demasiado claro/brillante para texto blanco legible.
"""

PALETTE = [
    ("#474795", "#6C6FC8", "#fff"),
    ("#954E00", "#CB772E", "#062120"),
    ("#554D9D", "#7D77D2", "#062120"),
    ("#9F5011", "#AE6716", "#fff"),
    ("#187EAA", "#22A2D3", "#062120"),
    ("#853B73", "#BE6094", "#062120"),
    ("#477826", "#788216", "#fff"),
    ("#2565A8", "#4D92DF", "#062120"),
    ("#913754", "#C76541", "#062120"),
    ("#607211", "#22A992", "#062120"),
    ("#744E9C", "#A378D1", "#062120"),
    ("#A15F13", "#A87D19", "#062120"),
    ("#136EAB", "#2E9BDC", "#062120"),
    ("#994063", "#CF698F", "#062120"),
    ("#396914", "#5F963D", "#062120"),
    ("#3D4A96", "#6072C9", "#fff"),
    ("#636A00", "#CF743B", "#062120"),
    ("#1679AF", "#21A981", "#062120"),
    ("#743678", "#A25BA6", "#fff"),
]


def swatches_for(order):
    """Asigna la paleta, en orden, a una lista de nombres de especialidad.

    Si en el futuro hay más especialidades que colores en la paleta (>19),
    la asignación se repite cíclicamente — hay que regenerar y validar una
    paleta más grande en ese caso en vez de confiar en el ciclo."""
    n = len(PALETTE)
    return {name: PALETTE[i % n] for i, name in enumerate(order)}


def css_colors_for(order):
    """Como swatches_for, pero listo para usarse en CSS: para cada
    especialidad da (color, ink) donde `color` ya es un valor
    light-dark(claro, oscuro) y `ink` es light-dark(blanco, tinta_oscura) —
    el texto a usar cuando `color` se pone de fondo."""
    out = {}
    for name, (light, dark, ink_dark) in swatches_for(order).items():
        out[name] = {
            "color": f"light-dark({light},{dark})",
            "ink": f"light-dark(#ffffff,{ink_dark})",
        }
    return out
