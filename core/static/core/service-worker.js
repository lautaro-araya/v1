const CACHE_NAME = "offline-cache-v1";
const urlsToCache = [
    "/",
    "/static/core/style_crearformulario.css",
    "/static/core/formulario_ofline.js",
   // "/static/core/logo.png",
];

// Instalar el Service Worker y cachear archivos
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(urlsToCache);
        })
    );
});

// Interceptar peticiones y servir desde caché si no hay internet
self.addEventListener("fetch", (event) => {
    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request))
    );
});