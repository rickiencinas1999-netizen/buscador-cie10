// Service worker del Buscador CIE-10.
// Cachea la app (que es un solo archivo HTML autocontenido, con los datos
// del catálogo incluidos) para que funcione sin conexión a internet una vez
// que se abrió por lo menos una vez — útil en zonas del hospital con mala
// señal de wifi.
//
// Sube CACHE_VERSION cada vez que se publique una nueva versión del
// catálogo/app para forzar a los navegadores a descargar la versión nueva.
const CACHE_VERSION = 'cie10-v2';
const SHELL = ['./', './index.html', './manifest.json', './icon-192.png', './icon-512.png'];

self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => cache.addAll(SHELL).catch(() => {}))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_VERSION).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  // El documento HTML principal (donde vive el catálogo) es lo único que
  // realmente cambia entre versiones. Para ese, red primero: si hay
  // internet, siempre se ve la versión más reciente publicada — incluso
  // abriendo la app desde el ícono de la pantalla de inicio, sin depender
  // de que el navegador detecte que hay un service worker nuevo. Solo si
  // no hay conexión (zonas del hospital con mala señal) se usa la copia
  // guardada como respaldo.
  const isDocument = event.request.mode === 'navigate' ||
    (event.request.headers.get('accept') || '').includes('text/html');
  if (isDocument) {
    event.respondWith(
      fetch(event.request)
        .then((resp) => {
          if (resp && resp.ok) {
            const copy = resp.clone();
            caches.open(CACHE_VERSION).then((cache) => cache.put(event.request, copy));
          }
          return resp;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // El resto (manifest, íconos) casi no cambia: cache-first con
  // actualización en segundo plano (stale-while-revalidate).
  event.respondWith(
    caches.match(event.request).then((cached) => {
      const network = fetch(event.request)
        .then((resp) => {
          if (resp && resp.ok) {
            const copy = resp.clone();
            caches.open(CACHE_VERSION).then((cache) => cache.put(event.request, copy));
          }
          return resp;
        })
        .catch(() => cached);
      return cached || network;
    })
  );
});
