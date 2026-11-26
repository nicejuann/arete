// Genuine eBible pack acceptance. Run only after the official archive builder succeeds.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const crypto=require('node:crypto');
const pack=JSON.parse(fs.readFileSync('bible-webp.json','utf8'));
const archive=fs.readFileSync('bible-source.zip');
assert.equal(pack.sourceSha256,crypto.createHash('sha256').update(archive).digest('hex'));
assert.equal(pack.books.length,66);
assert.equal(pack.books.reduce((n,b)=>n+b.chapters.length,0),1189);
assert.equal(pack.verseCount,pack.books.reduce((n,b)=>n+b.chapters.reduce((s,c)=>s+c.length,0),0));
assert.ok(pack.verseCount>=30000);
const verse=(code,ch,v)=>pack.books.find(b=>b.code===code).chapters[ch-1].find(x=>x.verse===v).text;
assert.match(verse('GEN',1,1),/in the beginning.*God.*created.*heaven.*earth/i);
assert.match(verse('JAS',1,5),/wisdom.*ask.*God/i);
assert.match(verse('REV',22,21),/grace.*(Lord|Jesus)/i);
(async()=>{
  const browser=await chromium.launch({headless:true});
  try{
    const context=await browser.newContext({viewport:{width:393,height:873},isMobile:true,hasTouch:true});
    const page=await context.newPage();
    const errors=[];page.on('pageerror',e=>errors.push(e.message));
    await context.route('**/*',r=>r.request().url().startsWith('http://127.0.0.1:8765/')?r.continue():r.abort());
    await page.goto('http://127.0.0.1:8765/',{waitUntil:'domcontentloaded'});
    await page.locator('.discovery-hub').waitFor();
    await page.waitForFunction(()=>!!navigator.serviceWorker.controller);
    await page.locator('#nav [data-tab="profile"]').click();
    await page.locator('input[data-topic="Faith"]').check();
    await page.locator('#nav [data-tab="library"]').click();
    await page.locator('[data-act="bible-open"]').click();
    await page.locator('[data-act="bible-pack-download"]:enabled').waitFor();
    await page.locator('[data-act="bible-pack-download"]').click();
    await page.locator('[data-act="bible-pack-remove"]').waitFor({timeout:90000});
    await page.locator('.bible-verses').waitFor();
    assert.match(await page.locator('.bible-verses').innerText(),/in the beginning.*God.*created.*heaven.*earth/i);
    console.log('Prepared pack loaded in Chromium: Genesis 1.');
    async function read(book,ch,pattern){
      await page.locator('#bible-book').selectOption(String(book));
      await page.locator('#bible-chapter').selectOption(String(ch));
      await page.locator('[data-act="bible-load"]').click();
      await page.locator('.bible-verses').waitFor();
      assert.match(await page.locator('.bible-verses').innerText(),pattern);
    }
    await read(58,1,/wisdom.*ask.*God/i);
    console.log('James 1 loaded; testing offline reload.');
    await context.setOffline(true);
    await page.reload({waitUntil:'domcontentloaded'});
    await page.locator('[data-act="bible-open"]').click();
    await page.locator('.bible-verses').waitFor();
    assert.match(await page.locator('.bible-verses').innerText(),/wisdom.*ask.*God/i);
    await read(65,22,/grace.*(Lord|Jesus)/i);
    // Remove the prepared pack, then exercise the real compressed ZIP import while offline.
    page.once('dialog',dialog=>dialog.accept());
    await page.locator('[data-act="bible-pack-remove"]').click();
    await page.locator('[data-act="bible-pack-import"]:enabled').waitFor();
    console.log('Prepared pack removed; testing original ZIP while offline.');
    await page.locator('#bible-pack-file').setInputFiles({name:'engwebp_vpl.zip',mimeType:'application/zip',buffer:archive});
    await page.locator('[data-act="bible-pack-remove"]').waitFor({timeout:90000});
    await page.locator('.bible-verses').waitFor();
    assert.match(await page.locator('.bible-verses').innerText(),/grace.*(Lord|Jesus)/i);
    const imported=await page.evaluate(()=>({books:biblePack.books.length,chapters:biblePack.books.reduce((n,b)=>n+b.chapters.length,0),count:biblePack.verseCount,localImport:biblePack.localImport,empty:biblePack.emptyReferences.length}));
    assert.deepEqual(imported,{books:66,chapters:1189,count:pack.verseCount,localImport:true,empty:pack.emptyReferences.length});
    const identical=await page.evaluate(expected=>JSON.stringify(biblePack.books)===JSON.stringify(expected.books)&&JSON.stringify(biblePack.emptyReferences)===JSON.stringify(expected.emptyReferences),{books:pack.books,emptyReferences:pack.emptyReferences});
    assert.ok(identical,'Imported archive and prepared pack differ');
    await read(0,1,/in the beginning.*God.*created.*heaven.*earth/i);
    assert.equal(errors.length,0,errors.join('\n'));
    console.log('Official eBible pack + compressed ZIP passed: source fingerprint, 66 books, 1189 chapters, '+pack.verseCount+' verses, offline Genesis/James/Revelation and local ZIP import.');
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
