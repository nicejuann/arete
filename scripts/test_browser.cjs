// Real Chromium mobile viewport smoke test; no external sources needed.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
// Stored ZIP with correct CRC-32, local headers and central directory.
function zipStored(entries){
  const locals=[],central=[];let offset=0;
  function crc32(b){let c=0xffffffff;for(const x of b){c^=x;for(let i=0;i<8;i++)c=(c>>>1)^((c&1)?0xedb88320:0)}return (c^0xffffffff)>>>0}
  for(const [name,value] of entries){
    const n=Buffer.from(name),d=Buffer.from(value),crc=crc32(d);
    const local=Buffer.alloc(30);local.writeUInt32LE(0x04034b50,0);local.writeUInt16LE(20,4);local.writeUInt32LE(crc,14);local.writeUInt32LE(d.length,18);local.writeUInt32LE(d.length,22);local.writeUInt16LE(n.length,26);
    const dir=Buffer.alloc(46);dir.writeUInt32LE(0x02014b50,0);dir.writeUInt16LE(20,4);dir.writeUInt16LE(20,6);dir.writeUInt32LE(crc,16);dir.writeUInt32LE(d.length,20);dir.writeUInt32LE(d.length,24);dir.writeUInt16LE(n.length,28);dir.writeUInt32LE(offset,42);
    locals.push(local,n,d);central.push(dir,n);offset+=local.length+n.length+d.length;
  }
  const c=Buffer.concat(central),end=Buffer.alloc(22);end.writeUInt32LE(0x06054b50,0);end.writeUInt16LE(entries.length,8);end.writeUInt16LE(entries.length,10);end.writeUInt32LE(c.length,12);end.writeUInt32LE(offset,16);
  return Buffer.concat([...locals,c,end]);
}

(async()=>{
  const browser=await chromium.launch({headless:true});
  try{
    const context=await browser.newContext({viewport:{width:393,height:873},isMobile:true,hasTouch:true,deviceScaleFactor:2});
    const page=await context.newPage();
    const errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    await page.route('**/*',r=>r.request().url().startsWith('http://127.0.0.1:8765/')?r.continue():r.abort());
    await page.goto('http://127.0.0.1:8765/',{waitUntil:'domcontentloaded'});
    await page.locator('.discovery-hub').waitFor();
    const lead=page.locator('.edition-lead');
    await lead.waitFor();
    const leadId=await lead.getAttribute('data-id');
    assert.ok(leadId);
    await lead.click();
    await page.locator('#post-'+leadId).waitFor();
    await page.locator('[data-act="focus-close"]').first().click();
    assert.equal(await page.locator('.edition-lead').getAttribute('data-id'),leadId);
    assert.equal(await page.locator('#nav svg').count(),5);
    await page.setViewportSize({width:320,height:720});
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1),'narrow screen horizontal overflow');
    await page.locator('#theme').click();
    assert.ok(await page.locator('body').evaluate(e=>e.classList.contains('light')));
    await page.locator('#theme').click();
    await page.setViewportSize({width:393,height:873});
    await page.locator('[data-act="focus"][data-focus="original"]').click();
    const first=page.locator('article.editorial').first();
    const id=await first.getAttribute('id');
    assert.ok(id);
    await first.locator('[data-act="save"]').click();
    await page.locator('[data-tab="saved"]').click();
    assert.equal(await page.locator('#'+id).count(),1);
    await page.reload();
    await page.locator('#'+id).waitFor();
    await page.locator('[data-tab="discover"]').click();
    await page.locator('[data-act="focus"][data-focus="original"]').click();
    await page.locator('[data-act="unread"]').click();
    const unread=page.locator('article.editorial').first();
    const unreadId=await unread.getAttribute('id');
    await unread.locator('[data-act="read"]').click();
    assert.equal(await page.locator('#'+unreadId).count(),0);
    await page.locator('[data-act="focus"][data-focus="quiz"]').click();
    await page.locator('.quiz-option').first().click();
    await page.locator('.quiz-answer').first().waitFor();
    const answeredId=await page.locator('.quiz-answer').first().locator('xpath=ancestor::article').getAttribute('id');
    assert.ok(await page.evaluate(id=>Object.hasOwn(JSON.parse(localStorage.getItem('arete-quiz-answers')),id.slice(5)),answeredId));
    await page.locator('.quiz-retry').first().click();
    assert.ok(await page.evaluate(id=>!Object.hasOwn(JSON.parse(localStorage.getItem('arete-quiz-answers')),id.slice(5)),answeredId));
    await page.locator('[data-tab="explore"]').click();
    await page.locator('#search').fill('moon');
    await page.locator('[data-act="search-open"]').first().click();
    await page.locator('[data-act="search-back"]').click();
    await page.locator('.search-hit').first().waitFor();
    await page.locator('[data-tab="discover"]').click();
    await page.locator('[data-act="focus"][data-focus="visual"]').click();
    await page.locator('.visual-intro').waitFor();
    await page.locator('article.compact-story').first().waitFor();
    assert.ok(await page.evaluate(()=>queue.every(p=>hasVisual(p))));
    await page.locator('[data-act="focus"][data-focus="media"]').click();
    await page.locator('.media-hub').waitFor();
    assert.equal(await page.locator('.media-player iframe').count(),0);
    await page.locator('[data-act="media-filter"][data-media-filter="audio"]').click();
    assert.ok(await page.locator('.media-tile').count()>0);
    assert.equal(await page.locator('.media-tile').filter({hasText:'Life on a Vent'}).count(),0);
    await page.locator('[data-tab="explore"]').click();
    await page.locator('#search').fill('');
    await page.locator('[data-act="guide-open"][data-guide="water"]').click();
    await page.locator('.guide-detail').waitFor();
    await page.locator('[data-act="guide-read"]').first().click();
    await page.locator('article.editorial').waitFor();
    await page.locator('[data-tab="profile"]').click();
    await page.locator('#voice-rate').selectOption('1.15');
    assert.equal(await page.evaluate(()=>localStorage.getItem('arete-voice-rate')),'1.15');
    await page.locator('#reading-size').selectOption('large');
    assert.ok(await page.locator('body').evaluate(e=>e.classList.contains('large-reading')));
    await page.locator('[data-tab="library"]').click();
    await page.locator('#book-file').setInputFiles({name:'test-book.txt',mimeType:'text/plain',buffer:Buffer.from('A sample personal book.\n\nSecond paragraph.')});
    await page.locator('.book-text').waitFor();
    assert.match(await page.locator('.book-text').innerText(),/sample personal book/);
    await page.locator('#book-search').fill('Second paragraph');
    await page.locator('.book-hit').first().click();
    assert.match(await page.locator('.book-text').innerText(),/Second paragraph/);
    await page.locator('[data-act="book-close"]').click();
    await page.locator('.human-track').first().waitFor();
    assert.equal(await page.locator('#human-player').count(),0);
    await page.locator('.human-track button').first().click();
    await page.locator('#human-player').waitFor({state:'attached'});
    await page.locator('[data-act="human-close"]').click();
    assert.equal(await page.locator('#human-player').count(),0);
    // Import a tiny standards-shaped EPUB using a test-only file.
    await page.locator('[data-tab="discover"]').click();
    await page.locator('[data-tab="library"]').click();
    const epub=zipStored([
      ['mimetype','application/epub+zip'],
      ['META-INF/container.xml','<?xml version="1.0"?><container xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>'],
      ['OEBPS/content.opf','<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0"><manifest><item id="a" href="a.xhtml" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="a"/></spine></package>'],
      ['OEBPS/a.xhtml','<?xml version="1.0"?><html xmlns="http://www.w3.org/1999/xhtml"><body><h1>Fixture chapter</h1><p>EPUB fixture paragraph.</p></body></html>']
    ]);
    await page.locator('#book-file').setInputFiles({name:'fixture.epub',mimeType:'application/epub+zip',buffer:epub});
    await page.locator('.book-text').waitFor();
    assert.match(await page.locator('.book-text').innerText(),/EPUB fixture paragraph/);
    // Test invalid Bible archive, then a full synthetic structure. No real Scripture is implied.
    await page.locator('[data-tab="profile"]').click();
    await page.locator('input[data-topic="Faith"]').check();
    await page.locator('[data-tab="library"]').click();
    await page.locator('[data-act="bible-open"]').click();
    await page.locator('#bible-pack-file').waitFor({state:'attached'});
    await page.waitForFunction(()=>!document.querySelector('[data-act="bible-pack-import"]').disabled);
    await page.locator('#bible-pack-file').setInputFiles({name:'engwebp_vpl.zip',mimeType:'application/zip',buffer:zipStored([['engwebp_vpl.txt','GEN 1:1 Synthetic fixture']])});
    await page.getByText('Incomplete or invalid archive:',{exact:false}).waitFor();
    const text=await page.evaluate(()=>PACK_CODES.flatMap((code,i)=>Array.from({length:BIBLE_BOOKS[i][1]},(_,j)=>Array.from({length:27},(_,v)=>code+' '+(j+1)+':'+(v+1)+' Synthetic fixture, not Scripture').join('\n')).join('\n')).join('\n'));
    await page.locator('#bible-pack-file').setInputFiles({name:'engwebp_vpl.zip',mimeType:'application/zip',buffer:zipStored([['engwebp_vpl.txt',text]])});
    await page.locator('[data-act="bible-pack-remove"]').waitFor();
    await page.locator('.bible-verses').waitFor();
    assert.match(await page.locator('.bible-verses').innerText(),/Synthetic fixture/);
    await page.locator('[data-tab="discover"]').click();
    await page.evaluate(async()=>{await navigator.serviceWorker.ready});
    await page.waitForFunction(()=>!!navigator.serviceWorker.controller);
    assert.ok(await page.evaluate(async()=>{const cache=await caches.open('arete-v2.0-rc27');const html=await cache.match(new URL('index.html',location.href));return html&&(await html.text()).includes('data-build="2.0-rc27"')}));
    assert.equal(await page.locator('#app-update').isVisible(),false);
    await context.setOffline(true);
    await page.reload({waitUntil:'domcontentloaded'});
    await page.locator('.discovery-hub').waitFor();
    assert.equal(await page.locator('#connection-status').innerText(),'Offline');
    await page.locator('[data-act="focus"][data-focus="new"]').click();
    assert.ok(await page.locator('#post-200').count()>0);
    await page.locator('[data-act="focus"][data-focus="original"]').click();
    await page.locator('article.editorial').first().waitFor();
    await page.locator('[data-tab="library"]').click();
    await page.locator('[data-act="bible-open"]').click();
    await page.locator('.bible-verses').waitFor();
    assert.match(await page.locator('.bible-verses').innerText(),/Synthetic fixture/);
    assert.equal(errors.length,0,errors.join('\n'));
    console.log('Mobile Chromium smoke test passed: navigation, saved persistence, unread, quiz, search, text size, TXT import and offline reload.');
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
