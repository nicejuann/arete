// ARETÉ: a version-matched offline shell, activated only when ready.
const VERSION='2.0-rc27';
const CACHE='arete-v'+VERSION;
const SHELL=['./index.html','./style.css?v='+VERSION,'./app.js?v='+VERSION,'./content.js?v='+VERSION];
const COLLECTIONS=['./fresh.json','./open-reading.json','./gallery.json'];
const ASSETS=['./manifest.webmanifest','./icon.svg','./icon-192.png','./icon-512.png'];
const absolute=path=>new URL(path,self.registration.scope).href;
function isVersionedAsset(url){const u=new URL(url);return ['app.js','content.js','style.css'].some(name=>u.pathname===new URL(name,self.registration.scope).pathname)&&/^2\.0-rc\d+$/.test(u.searchParams.get('v')||'')}
async function checkedShell(path){
  const response=await fetch(new Request(absolute(path),{cache:'reload'}));
  if(!response.ok)throw Error('Shell HTTP failure: '+path);
  const text=await response.clone().text();
  const marker=path.endsWith('index.html')?'data-build="'+VERSION+'"':'/* ARETE_BUILD:'+VERSION+' */';
  if(!text.includes(marker))throw Error('Version mismatch: '+path);
  return [absolute(path),response];
}
self.addEventListener('install',event=>event.waitUntil((async()=>{
  try{
    const verified=await Promise.all(SHELL.map(checkedShell));
    const c=await caches.open(CACHE);
    for(const [url,response] of verified)await c.put(url,response);
    await c.addAll([...COLLECTIONS,...ASSETS].map(path=>new Request(absolute(path),{cache:'reload'})));
    // No skipWaiting here: the previous release remains usable until activation.
  }catch(error){await caches.delete(CACHE);throw error}
})()));
self.addEventListener('message',event=>{if(event.data?.type==='ARETE_ACTIVATE_UPDATE')event.waitUntil(self.skipWaiting())});
self.addEventListener('activate',event=>event.waitUntil((async()=>{
  const keys=await caches.keys();
  // Retain one previous release to help a still-open old page resolve its assets.
  const old=keys.filter(k=>/^arete-v2\.0-rc\d+$/.test(k)&&k!==CACHE&&Number(k.split('rc').pop())<Number(VERSION.split('rc').pop())).sort((a,b)=>Number(b.split('rc').pop())-Number(a.split('rc').pop()));
  await Promise.all(old.slice(1).map(k=>caches.delete(k)));
  await self.clients.claim();
})()));
async function respond(request){
  const c=await caches.open(CACHE);
  // A controlled navigation always receives the same HTML as this worker's assets.
  if(request.mode==='navigate')return await c.match(absolute('./index.html'))||Response.error();
  const url=new URL(request.url);
  if(COLLECTIONS.some(path=>url.pathname===new URL(path,self.registration.scope).pathname)){
    try{const response=await fetch(request,{cache:'no-cache'});if(response.ok){await c.put(request,response.clone());return response}}catch{}
    return await c.match(request)||Response.error();
  }
  const hit=await c.match(request);if(hit)return hit;
  if(isVersionedAsset(request.url)){
    // Never substitute another release's JS/CSS from the network.
    const versions=(await caches.keys()).filter(k=>/^arete-v2\.0-rc\d+$/.test(k)&&k!==CACHE);
    for(const key of versions){const old=await (await caches.open(key)).match(request);if(old)return old}
    return Response.error();
  }
  try{return await fetch(request)}catch{return Response.error()}
}
self.addEventListener('fetch',event=>{const r=event.request;if(r.method!=='GET'||new URL(r.url).origin!==self.location.origin||!r.url.startsWith(self.registration.scope))return;event.respondWith(respond(r))});
