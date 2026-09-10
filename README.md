# Buscador CIE-10 por especialidad

Catálogo curado de diagnósticos CIE-10, organizado por especialidad médica y
categoría clínica, pensado para uso hospitalario: encontrar rápido el código
correcto sin tener que buscar entre miles de entradas del catálogo maestro.

El proyecto tiene dos salidas, generadas a partir de la misma fuente de datos:

1. **App web de búsqueda** (`webapp/index.html`) — un solo archivo HTML
   autocontenido (sin dependencias de red, sin backend) que se puede abrir
   con doble clic o publicar en cualquier hosting estático (GitHub Pages,
   una intranet, etc.). Permite buscar por código o por nombre del
   diagnóstico, y filtrar por especialidad.
2. **Póster imprimible** (`dist/poster.pdf`) — infografía en hojas tamaño
   carta horizontal, pensada para pegarse en un pizarrón frente a las
   computadoras, con los diagnósticos agrupados por especialidad y
   categoría clínica.

## Estructura del repositorio

```
data/
  catalogo.json          Catálogo maestro CIE-10 completo (código -> datos),
                          extraído del Excel institucional oficial.
src/
  especialidades.py      Fuente de verdad: códigos CIE-10 curados por
                          especialidad y categoría clínica. Valida cada
                          código contra data/catalogo.json al importarse.
  generar_datos_app.py   Genera dist/app_data.json (catálogo completo +
                          etiquetas de especialidad) para la app web.
  plantilla_app.html     Plantilla HTML/CSS/JS de la app de búsqueda.
  construir_app.py       Combina la plantilla + dist/app_data.json en
                          webapp/index.html (archivo único autocontenido).
  generar_poster.py      Genera dist/poster.html (el póster, paginado
                          automáticamente por especialidad).
  generar_pdf.js         Convierte dist/poster.html a dist/poster.pdf
                          usando Playwright + Chromium.
webapp/
  index.html              App de búsqueda ya generada, lista para usar.
dist/
  app_data.json           Datos generados (intermedio).
  poster.html              Póster generado (intermedio).
  poster.pdf                Póster final en PDF (se genera con Node/Playwright).
  report.json              Reporte de validación de especialidades.py.
```

## Cómo actualizar el catálogo curado

Todo el contenido clínico (qué código pertenece a qué especialidad y
categoría) vive en **`src/especialidades.py`**. Para agregar, quitar o mover
códigos, edita el diccionario `SPECIALTIES` de ese archivo y vuelve a correr
el pipeline (ver abajo). Cada código se valida automáticamente contra
`data/catalogo.json`; si un código no existe en el catálogo o está
duplicado dentro de la misma especialidad, se imprime un aviso al correr
el script.

## Cómo regenerar todo

Requiere Python 3 (sin dependencias externas) y, solo para el PDF, Node.js
con Playwright.

```bash
cd buscador-cie10

# 1. Datos para la app web (a partir de especialidades.py + catalogo.json)
python3 src/generar_datos_app.py

# 2. App web autocontenida (webapp/index.html)
python3 src/construir_app.py

# 3. Póster en HTML (dist/poster.html)
python3 src/generar_poster.py

# 4. Póster en PDF (dist/poster.pdf) — opcional, requiere Node + Playwright
npm install
npx playwright install chromium
npm run pdf
```

Cada script es independiente y se puede correr por separado siempre que
los archivos de los que depende ya existan (ver diagrama de dependencias
arriba). `webapp/index.html` y `dist/poster.pdf` ya vienen generados en
este repositorio, así que no es necesario correr nada para usarlos tal
cual — el pipeline solo es necesario cuando se actualiza el catálogo
curado.

## Cómo usar la app de búsqueda

Abre `webapp/index.html` en cualquier navegador (doble clic, o súbelo a un
servidor/hosting estático). No requiere internet ni instalación, salvo la
carga de tipografías desde Google Fonts si hay conexión disponible (si no
la hay, usa las tipografías del sistema).

## Cómo imprimir el póster

Imprime `dist/poster.pdf` en tamaño carta, orientación horizontal, sin
márgenes ("sin escala" / "tamaño real" en el diálogo de impresión).
