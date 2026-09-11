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

// Cache-first con actualización en segundo plano (stale-while-revalidate):
// responde rápido desde cache y, si hay red, refresca la cache para la
// siguiente visita.
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
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
