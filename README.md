# Buscador CIE-10 por especialidad

Catálogo curado de diagnósticos CIE-10, organizado por especialidad médica y
categoría clínica, pensado para uso hospitalario: encontrar rápido el código
correcto sin tener que buscar entre miles de entradas del catálogo maestro.

El proyecto tiene dos salidas, generadas a partir de la misma fuente de datos:

1. **App web de búsqueda** (`webapp/index.html`) — un solo archivo HTML
   autocontenido (sin dependencias de red, sin backend) que se puede abrir
   con doble clic o publicar en cualquier hosting estático (GitHub Pages,
   Render, una intranet, etc.). Permite buscar por código, por nombre del
   diagnóstico o por **palabra clave/síntoma/abreviatura** (p. ej. "dolor de
   pecho", "IAM", "IVU"), y filtrar por especialidad. Además es una PWA
   instalable: se puede "agregar a inicio" en teléfono, tablet o
   computadora y funciona sin conexión una vez abierta la primera vez.
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
  especialidades.py      Fuente de verdad clínica: códigos CIE-10 curados
                          por especialidad y categoría. Valida cada código
                          contra data/catalogo.json al importarse.
  sinonimos.py            Fuente de verdad de búsqueda: palabras clave,
                          síntomas y abreviaturas -> códigos CIE-10 (p. ej.
                          "dolor de pecho" o "IAM" -> infarto). También se
                          valida contra data/catalogo.json.
  generar_datos_app.py   Genera dist/app_data.json (catálogo completo +
                          etiquetas de especialidad + sinónimos) para la
                          app web.
  plantilla_app.html     Plantilla HTML/CSS/JS de la app de búsqueda.
  construir_app.py       Combina la plantilla + dist/app_data.json en
                          webapp/index.html (archivo único autocontenido).
  generar_poster.py      Genera dist/poster.html (el póster, paginado
                          automáticamente por especialidad).
  generar_pdf.js         Convierte dist/poster.html a dist/poster.pdf
                          usando Playwright + Chromium.
  generar_qr.py           Genera dist/qr.png con el QR de la URL donde
                          quede publicada la app.
webapp/
  index.html              App de búsqueda ya generada (autocontenida).
  manifest.json            Metadatos de instalación (PWA).
  sw.js                     Service worker: cachea la app para uso sin
                          conexión y habilita "instalarla" como app.
  icon-192.png, icon-512.png   Íconos de la app (PWA).
  hospital-logo.png         Logo institucional (CIMA), se muestra junto
                          al nombre de la app. Para cambiarlo, reemplaza
                          este archivo (y su copia en docs/) por otro PNG
                          y corre construir_app.py.
docs/
  (espejo exacto de webapp/, mismos archivos) — existe solo porque
  GitHub Pages en modo "Deploy from a branch" únicamente puede publicar
  la raíz del repo o una carpeta llamada "docs". Se regenera solo al
  correr construir_app.py.
dist/
  app_data.json           Datos generados (intermedio).
  poster.html              Póster generado (intermedio).
  poster.pdf                Póster final en PDF (se genera con Node/Playwright).
  qr.png                    QR de la app publicada (se genera aparte).
  report.json              Reporte de validación de especialidades.py.
.github/workflows/
  deploy-pages.yml         Publica webapp/ en GitHub Pages automáticamente.
render.yaml               Blueprint para publicar webapp/ en Render.
```

## Cómo actualizar el catálogo curado

Todo el contenido clínico (qué código pertenece a qué especialidad y
categoría) vive en **`src/especialidades.py`**. Para agregar, quitar o mover
códigos, edita el diccionario `SPECIALTIES` de ese archivo y vuelve a correr
el pipeline (ver abajo). Cada código se valida automáticamente contra
`data/catalogo.json`; si un código no existe en el catálogo o está
duplicado dentro de la misma especialidad, se imprime un aviso al correr
el script.

## Cómo agregar palabras clave / síntomas a la búsqueda

La búsqueda "inteligente" (escribir "dolor de pecho" y que aparezca
infarto, escribir "IVU" y que aparezca infección urinaria) vive en
**`src/sinonimos.py`**, en el diccionario `SYNONYMS`. Cada entrada es
`"término coloquial o abreviatura": ["CODIGO1", "CODIGO2", ...]`. Para
agregar más, solo agrega una línea nueva y vuelve a correr el pipeline —
igual que con `especialidades.py`, los códigos se validan automáticamente
contra `data/catalogo.json` al importar el archivo.

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
la hay, usa las tipografías del sistema). Una vez publicada en un sitio
real (ver abajo), en el teléfono/tablet se puede "Agregar a pantalla de
inicio" (Android/Chrome) o "Agregar a inicio" (iPhone/Safari) y queda
como una app más, con su propio ícono, y sigue funcionando sin conexión.

## Cómo imprimir el póster

Imprime `dist/poster.pdf` en tamaño carta, orientación horizontal, sin
márgenes ("sin escala" / "tamaño real" en el diálogo de impresión).

## Cómo publicarla (GitHub Pages y/o Render)

Este repositorio ya viene listo para publicarse en cualquiera de las dos
opciones (se puede usar una sola, o ambas). No requieren build: la app ya
está generada en `webapp/`.

### Opción A — GitHub Pages (gratis)

1. Sube este repositorio a GitHub (ver instrucciones al final de este
   documento si no sabes cómo).
2. En el repo, entra a **Settings -> Pages** y en **"Source"** elige
   **"Deploy from a branch"**. Justo abajo aparecen dos menús: en el
   primero elige la rama **`main`**, y en el segundo (que por default dice
   `/ (root)`) elige **`/docs`**. Guarda con **Save**.
3. Espera 1-2 minutos. La URL final aparece arriba en esa misma página de
   **Settings -> Pages** (con este formato:
   `https://tu-usuario.github.io/buscador-cie10/`).

Este método publica directamente el contenido de la carpeta `docs/` (que
`construir_app.py` mantiene idéntico a `webapp/`) sin depender de GitHub
Actions, así que no hace falta preocuparse por permisos de Actions ni por
verificar el correo de la cuenta.

Con cada actualización del catálogo, después de correr `construir_app.py`
y hacer `git push`, GitHub Pages recoge el cambio de `docs/` automáticamente.

*(Este repositorio también incluye `.github/workflows/deploy-pages.yml`,
una forma alterna de publicar con GitHub Actions eligiendo "Source: GitHub
Actions" en vez de "Deploy from a branch" — pero solo hace falta uno de
los dos métodos; si "Deploy from a branch" con `/docs` ya te funciona, no
hace falta tocar el de Actions.)

### Opción B — Render

1. Sube el repositorio a GitHub (igual que arriba).
2. En [render.com](https://render.com), **New -> Blueprint**, conecta el
   repositorio: Render detecta `render.yaml` automáticamente y crea un
   "Static Site" que publica `webapp/`.
   - Alternativa sin blueprint: **New -> Static Site**, conecta el repo,
     dejar "Build Command" vacío y poner **Publish Directory: `webapp`**.
3. Render te da una URL del tipo `https://buscador-cie10.onrender.com`.

### Código QR para el pizarrón

Una vez que tengas la URL final (de GitHub Pages o de Render), genera el
QR para imprimir junto al póster:

```bash
pip install qrcode[pil]
python3 src/generar_qr.py https://tu-usuario.github.io/buscador-cie10/
```

Esto guarda `dist/qr.png`, listo para pegarlo en el pizarrón junto al
póster: cualquiera lo escanea con el teléfono y abre el buscador
directamente.

### Cómo subir este repositorio a GitHub

Este repositorio ya viene con `git init` hecho y el primer commit listo.
Solo falta conectarlo a un repositorio remoto en GitHub:

1. En [github.com](https://github.com), crea un repositorio nuevo, **vacío**
   (sin README, sin .gitignore — ya los trae este repo), por ejemplo
   llamado `buscador-cie10`.
2. Desde una terminal, dentro de esta carpeta:

```bash
git remote add origin https://github.com/TU_USUARIO/buscador-cie10.git
git branch -M main
git push -u origin main
```

A partir de ahí, cualquier cambio (por ejemplo editar
`src/especialidades.py` o `src/sinonimos.py`, regenerar y hacer
`git commit` + `git push`) se refleja automáticamente en GitHub Pages, y
Render lo redetecta también si está conectado al mismo repo.
