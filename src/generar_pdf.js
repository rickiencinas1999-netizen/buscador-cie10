// Convierte dist/poster.html -> dist/poster.pdf usando Playwright + Chromium.
//
// Requiere: npm install playwright   (y los binarios de Chromium instalados,
// p. ej. `npx playwright install chromium`)
//
// Si Chromium ya está instalado en una ruta fija (como en este entorno de
// desarrollo, /opt/pw-browsers/chromium), se puede fijar con la variable de
// entorno PW_CHROMIUM_PATH; si no se define, Playwright usa su propio
// Chromium administrado.
//
// Uso (desde la raíz del repo, después de correr generar_poster.py):
//   node src/generar_pdf.js

const { chromium } = require('playwright');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const HTML_PATH = path.join(ROOT, 'dist', 'poster.html');
const PDF_PATH = path.join(ROOT, 'dist', 'poster.pdf');

(async () => {
  const launchOpts = {};
  if (process.env.PW_CHROMIUM_PATH) {
    launchOpts.executablePath = process.env.PW_CHROMIUM_PATH;
  }
  const browser = await chromium.launch(launchOpts);
  const page = await browser.newPage();
  const fileUrl = 'file://' + HTML_PATH;
  await page.goto(fileUrl, { waitUntil: 'networkidle' });
  await page.pdf({
    path: PDF_PATH,
    width: '11in',
    height: '8.5in',
    printBackground: true,
    margin: { top: '0', bottom: '0', left: '0', right: '0' },
  });
  await browser.close();
  console.log('PDF listo:', PDF_PATH);
})();
