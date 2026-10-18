const SHELL_CACHE = 'ddclient-shell-v1';
const DATA_CACHE = 'ddclient-data-v1';
const ASSETS = [
    './',
    './index.html',
    './css.css',
    './app.js',
    './manifest.webmanifest',
    './icon.svg',
];
const DATA_ASSETS = [
    './data/conditions.json',
    './data/symptoms.json',
    './data/tests.json',
    './data/citations.json',
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        (async () => {
            const shell = await caches.open(SHELL_CACHE);
            await shell.addAll(ASSETS);
            const data = await caches.open(DATA_CACHE);
            try {
                await data.addAll(DATA_ASSETS);
            } catch {
                // Data precaching is best effort: the app reports invalid data itself.
            }
        })(),
    );
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches
            .keys()
            .then((keys) =>
                Promise.all(
                    keys
                        .filter((key) => key !== SHELL_CACHE && key !== DATA_CACHE)
                        .map((key) => caches.delete(key)),
                ),
            ),
    );
    self.clients.claim();
});

function isDataCollection(url) {
    return (
        /\/data\/[^/]+\.json$/.test(url.pathname) && !url.pathname.endsWith('/data/version.json')
    );
}

async function refresh(cache, request) {
    const response = await fetch(request);
    if (response.ok) await cache.put(request, response.clone());
    return response;
}

async function serveData(request) {
    const cache = await caches.open(DATA_CACHE);
    const bypass = request.cache === 'no-store' || request.cache === 'reload';
    if (!bypass) {
        const cached = await cache.match(request);
        if (cached) return cached;
    }
    return refresh(cache, request);
}

self.addEventListener('fetch', (event) => {
    if (event.request.method !== 'GET') return;
    const url = new URL(event.request.url);
    if (url.origin !== self.location.origin) return;
    if (isDataCollection(url)) {
        event.respondWith(serveData(event.request));
        return;
    }
    if (url.pathname.endsWith('/data/version.json')) return;
    event.respondWith(
        caches
            .open(SHELL_CACHE)
            .then((cache) =>
                cache.match(event.request).then((cached) => cached || fetch(event.request)),
            ),
    );
});
