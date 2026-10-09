/* Service worker van de bestellingenportal.
   Hij doet twee dingen: de app mag op het beginscherm staan, en een melding
   die je aantikt opent de portal in plaats van een nieuw tabblad. */

const BAK = "koekenbakker-portal-v2";
const SCHIL = ["./", "./index.html", "./manifest.json", "./icoon-512.png"];

self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(BAK).then(function (bak) { return bak.addAll(SCHIL); }));
  self.skipWaiting();
});

self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (namen) {
    return Promise.all(namen.filter(function (n) { return n !== BAK; })
                            .map(function (n) { return caches.delete(n); }));
  }).then(function () { return self.clients.claim(); }));
});

/* Netwerk eerst — bestellingen moeten altijd vers zijn. Lukt dat niet, dan de
   bewaarde versie, zodat de portal ook zonder bereik opent. */
self.addEventListener("fetch", function (e) {
  if (e.request.method !== "GET" || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(
    fetch(e.request).then(function (antwoord) {
      const kopie = antwoord.clone();
      caches.open(BAK).then(function (bak) { bak.put(e.request, kopie); });
      return antwoord;
    }).catch(function () { return caches.match(e.request); })
  );
});

/* Een aangetikte melding opent de portal die al openstaat. */
self.addEventListener("notificationclick", function (e) {
  e.notification.close();
  e.waitUntil(clients.matchAll({type: "window", includeUncontrolled: true}).then(function (lijst) {
    for (const c of lijst) if (c.url.indexOf("/bestellingen") > -1 && "focus" in c) return c.focus();
    if (clients.openWindow) return clients.openWindow("./");
  }));
});
