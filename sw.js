const CACHE='arete-v0.5';
const FILES=['./','./index.html','./style.css?v=0.5','./app.js?v=0.5','./content.js?v=0.5','./manifest.webmanifest','./icon.svg','./icon-192.png','./icon-512.png'];
self.addEventListener('install',e=>e.waitUntil((async()=>{const c=await caches.open(CACHE);await c.addAll(FILES.map(path=>new Request(new URL(path,self.registration.scope),{cache:'reload'})));await self.skipWaiting()})()));
self.addEventListener('activate',e=>e.waitUntil((async()=>{const keys=await caches.keys();await Promise.all(keys.filter(k=>k.startsWith('arete-')&&k!==CACHE).map(k=>caches.delete(k)));await self.clients.claim()})()));
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||new URL(r.url).origin!==self.location.origin||!r.url.startsWith(self.registration.scope))return;
e.respondWith((async()=>{const c=await caches.open(CACHE);if(r.mode==='navigate'){try{const n=await fetch(r,{cache:'no-cache'});if(n.ok)return n;}catch{}return await c.match('./index.html')||Response.error()}
const hit=await c.match(r);if(hit)return hit;try{return await fetch(r)}catch{return Response.error()}})())});
