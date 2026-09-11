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

Ajuste posterior (croma más bajo): la primera versión usaba croma alto
(~0.115-0.135) para maximizar la separación — quedaba muy distinguible pero
se veía como "muchos colores vivos que no combinan entre sí". Se bajó el
croma objetivo a ~0.115-0.12 (el mínimo que sigue pasando los mismos
checks — se probó cada escalón contra el validador real hasta encontrarlo)
para que los 19 tonos se vean como una familia coordinada de colores
apagados/tipo "joya" en vez de un arcoíris de colores saturados, sin dejar
de distinguirse entre sí.

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
    ("#8A3346", "#B65E6D", "#fff"),
    ("#2C783B", "#5DA467", "#062120"),
    ("#58519E", "#7F7BC8", "#062120"),
    ("#9A5A12", "#AD6C29", "#fff"),
    ("#188468", "#21A696", "#062120"),
    ("#873F75", "#9C71B9", "#062120"),
    ("#6A7312", "#7B8529", "#062120"),
    ("#2C68A8", "#5A94D5", "#062120"),
    ("#8F3C62", "#BD6F43", "#062120"),
    ("#806A12", "#1B917D", "#062120"),
    ("#76529D", "#A17EC9", "#062120"),
    ("#946D14", "#A87F23", "#062120"),
    ("#1573A7", "#1A89B2", "#062120"),
    ("#9A4566", "#CB7184", "#062120"),
    ("#3D6C1D", "#67954C", "#062120"),
    ("#404E97", "#6677C1", "#fff"),
    ("#9B4E1A", "#C87A4D", "#062120"),
    ("#198868", "#219C7B", "#062120"),
    ("#763A79", "#866DB8", "#fff"),
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
