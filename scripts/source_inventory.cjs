const fs=require('node:fs'),vm=require('node:vm');
const originals=vm.runInNewContext(fs.readFileSync('content.js','utf8')+'\nCONTENT');
const sources=new Map();
function add(url,role,id,title){
  if(typeof url!=='string')return;
  let u;try{u=new URL(url)}catch{return}
  if(u.protocol!=='https:'||u.username||u.password||!u.hostname.includes('.'))return;
  u.hash='';
  const key=u.href,ref={role,id:String(id??''),title:String(title??'')};
  if(!sources.has(key))sources.set(key,{url:key,refs:[]});
  const record=sources.get(key);if(!record.refs.some(r=>r.role===ref.role&&r.id===ref.id&&r.title===ref.title))record.refs.push(ref);
}
function buildInventory(){
  for(const p of originals){
    add(p.url,'original source',p.id,p.title);
    if(p.photo){add(p.photo[0],'image',p.id,p.title);add(p.photo[3],'image credit',p.id,p.title)}
    if(p.media)add(p.media[2],'media source',p.id,p.title);
    if(p.video)add(p.video,'video file',p.id,p.title);
  }
  for(const [file,role] of [['fresh.json','headline'],['open-reading.json','open reading'],['gallery.json','museum record']]){
    const data=JSON.parse(fs.readFileSync(file,'utf8'));
    for(const p of data.items){add(p.url,role,p.id,p.title);if(p.image)add(p.image,'image',p.id,p.title);if(p.revision)add(p.revision,'revision',p.id,p.title);if(p.history)add(p.history,'history',p.id,p.title)}
  }
  // App-only library and media sources: static URL literals, not constructed endpoints.
  for(const m of fs.readFileSync('app.js','utf8').matchAll(/https:\/\/[^\s"'<>\\]+/g)){
    const url=m[0].replace(/[),;\]]+$/,'');
    if(/[$\{\}]/.test(url)||/\/$/.test(url)&&/bible-api\.com|cdn\.jsdelivr\.net/.test(url))continue;
    if(/\.(mp3|ogg|m4a)(?:\?|$)/i.test(url)&&!/^https:\/\/[^/]+\/wiki\/File:/i.test(url))add(url,'audio file','','');
    else if(!sources.has(url))add(url,'app resource','','');
  }
  const records=[...sources.values()].sort((a,b)=>a.url.localeCompare(b.url));
  const review=originals.map(p=>({id:p.id,category:p.category,title:p.title,words:[p.summary,p.body,p.extra].filter(Boolean).join(' ').trim().split(/\s+/).length,source:p.source,url:p.url,hasQuiz:!!p.quiz,hasPhoto:!!p.photo,review:p.editorialReview?.status||'not reviewed',reviewDate:p.editorialReview?.date||'',reviewScope:p.editorialReview?.scope||''}));
  const csv=v=>'"'+String(v??'').replace(/"/g,'""')+'"';
  const columns=['id','category','title','words','source','url','hasQuiz','hasPhoto','review','reviewDate','reviewScope'];
  fs.writeFileSync('source-inventory.json',JSON.stringify({originals:review.length,links:records},null,2)+'\n');
  fs.writeFileSync('editorial-review.csv',[columns.join(','),...review.map(p=>columns.map(k=>csv(p[k])).join(','))].join('\n')+'\n');
  console.log(JSON.stringify({originals:review.length,uniqueLinks:records.length,under120Words:review.filter(p=>p.words<120).length,sourceAligned:review.filter(p=>p.review==='source-aligned revision').length}));
  return {review,records};
}
buildInventory();
