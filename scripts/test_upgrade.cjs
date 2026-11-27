// Real browser upgrade using the exact preceding committed files.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const http=require('node:http');
const {execFileSync}=require('node:child_process');
const OLD_COMMIT='585d9c03b198880411f3653a5a276fdd2c9f0d90';
const OLD='2.0-rc38',NEXT='2.0-rc39';
const files=['index.html','style.css','app.js','content.js','sw.js','fresh.json','open-reading.json','gallery.json','manifest.webmanifest','icon.svg','icon-192.png','icon-512.png'];
const old=new Map(files.map(p=>[p,execFileSync('git',['show',OLD_COMMIT+':'+p],{maxBuffer:20*1024*1024})]));
const current=new Map(files.map(p=>[p,fs.readFileSync(p)]));
const types={html:'text/html; charset=utf-8',js:'application/javascript; charset=utf-8',css:'text/css; charset=utf-8',json:'application/json',webmanifest:'application/manifest+json',svg:'image/svg+xml',png:'image/png'};
let release=old;
const server=http.createServer((req,res)=>{
  const pathname=new URL(req.url,'http://localhost').pathname;
  const file=pathname==='/'?'index.html':pathname.slice(1);
  if(!release.has(file)){res.writeHead(404);res.end();return}
  res.writeHead(200,{'Content-Type':types[file.split('.').pop()]||'application/octet-stream','Cache-Control':'no-store'});
  res.end(release.get(file));
});
(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const url='http://127.0.0.1:'+server.address().port+'/';
  const browser=await chromium.launch({headless:true});
  try{
    const context=await browser.newContext({viewport:{width:393,height:873},isMobile:true,hasTouch:true,deviceScaleFactor:2});
    const page=await context.newPage(),errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    await context.route('**/*',route=>route.request().url().startsWith(url)?route.continue():route.abort());
    await page.goto(url,{waitUntil:'domcontentloaded'});
    await page.locator('.discovery-hub').waitFor();
    await page.waitForFunction(()=>!!navigator.serviceWorker.controller);
    assert.equal(await page.locator('html').getAttribute('data-build'),OLD);
    await page.locator('[data-act="focus"][data-focus="original"]').click();
    const first=page.locator('article.editorial').first(),post=await first.getAttribute('id');
    await first.locator('[data-act="save"]').click();
    await first.locator('[data-act="expand"]').click();
    await first.locator('textarea').fill('Upgrade preservation fixture');
    const id=Number(post.slice(5));
    const quiz=await page.evaluate(()=>{const p=CONTENT.find(x=>x.quiz);rememberQuiz(p,p.quiz[2]);return p.id});
    const before=await page.evaluate(()=>({saved:JSON.parse(localStorage.getItem('arete-v1')).saved,notes:JSON.parse(localStorage.getItem('arete-v1')).notes,quiz:JSON.parse(localStorage.getItem('arete-quiz-answers'))}));
    assert.ok(before.saved.includes(id)&&before.notes[id]==='Upgrade preservation fixture'&&Object.hasOwn(before.quiz,quiz));
    release=current;
    await page.evaluate(async()=>{const reg=await navigator.serviceWorker.ready;await reg.update()});
    await page.waitForFunction(async()=>!!(await navigator.serviceWorker.getRegistration()).waiting,{},{timeout:30000});
    await page.locator('#app-update').waitFor({state:'visible',timeout:30000});
    assert.equal(await page.locator('html').getAttribute('data-build'),OLD);
    // Active worker must still serve the old coherent release before acceptance.
    await page.reload({waitUntil:'domcontentloaded'});
    await page.locator('#app-update').waitFor({state:'visible'});
    assert.equal(await page.locator('html').getAttribute('data-build'),OLD);
    await page.locator('[data-act="app-update"]').click();
    await page.waitForFunction(next=>document.documentElement.dataset.build===next,NEXT,{timeout:30000});
    await page.locator('.discovery-hub').waitFor();
    const after=await page.evaluate(()=>({saved:JSON.parse(localStorage.getItem('arete-v1')).saved,notes:JSON.parse(localStorage.getItem('arete-v1')).notes,quiz:JSON.parse(localStorage.getItem('arete-quiz-answers'))}));
    assert.deepEqual(after,before);
    assert.ok(await page.evaluate(async old=> (await caches.keys()).includes('arete-v'+old),OLD));
    await context.setOffline(true);
    await page.reload({waitUntil:'domcontentloaded'});
    await page.locator('.discovery-hub').waitFor();
    assert.equal(await page.locator('html').getAttribute('data-build'),NEXT);
    assert.equal(await page.locator('#connection-status').innerText(),'Offline');
    await page.locator('[data-tab="saved"]').click();
    await page.locator('#'+post).waitFor();
    await page.locator('#'+post+' [data-act="expand"]').click();
    assert.equal(await page.locator('#'+post+' textarea').inputValue(),'Upgrade preservation fixture');
    assert.equal(errors.length,0,errors.join('\n'));
    console.log('RC38 to RC39: actual prior release, waiting worker, explicit activation, old shell before activation, saved article/note/quiz preservation, previous cache and offline reload passed.');
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1}).finally(()=>server.close());
