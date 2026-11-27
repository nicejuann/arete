'use strict';
// Mechanical editorial triage only: neither factual verification nor peer review.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const norm=s=>String(s??'').normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{N}\s]/gu,' ').trim().replace(/\s+/g,' ');
const words=s=>String(s??'').trim().split(/\s+/).filter(Boolean);
const body=p=>[p.summary,p.body,p.extra].filter(Boolean).join(' ');
const https=s=>{try{const u=new URL(s);return u.protocol==='https:'&&!u.username&&!u.password&&u.hostname.includes('.')}catch{return false}};
function audit(posts){
  const failures=[],categories={},sentences=new Map(),titles=new Map(),prompts=new Map(),reviewMissing=[],quizIssues=[],missingReflection=[],nearPairs=[];
  const add=(m,k,id)=>{if(!m.has(k))m.set(k,new Set());m.get(k).add(id)};
  const duplicates=m=>[...m].filter(([,ids])=>ids.size>1).map(([text,ids])=>({text,ids:[...ids]}));
  const grams=s=>{const w=words(norm(s)),g=new Set();for(let i=0;i+4<w.length;i++)g.add(w.slice(i,i+5).join(' '));return g};
  let totalWords=0,minWords=Infinity,maxWords=0,quizCount=0;
  const seen=new Set(),vectors=[];
  for(const p of posts){
    if(!Number.isInteger(p.id)||seen.has(p.id))failures.push({id:p.id,issue:'invalid or duplicate ID'});seen.add(p.id);
    for(const key of ['title','category','summary','body','extra','source'])if(typeof p[key]!=='string'||!p[key].trim())failures.push({id:p.id,issue:'missing '+key});
    if(!https(p.url))failures.push({id:p.id,issue:'invalid source URL'});
    const n=words(body(p)).length;totalWords+=n;minWords=Math.min(minWords,n);maxWords=Math.max(maxWords,n);if(n<300)failures.push({id:p.id,issue:'under 300 words'});
    categories[p.category]=(categories[p.category]||0)+1;
    if(p.editorialReview?.status!=='source-aligned revision'||!/^\d{4}-\d{2}-\d{2}$/.test(p.editorialReview?.date||'')||!p.editorialReview?.scope)reviewMissing.push(p.id);
    add(titles,norm(p.title),p.id);
    if(typeof p.reflection!=='string'||!p.reflection.trim())missingReflection.push(p.id);else add(prompts,norm(p.reflection),p.id);
    for(const s of (String(p.body??'')+'\n'+String(p.extra??'')).split(/(?<=[.!?])\s+/)){const k=norm(s);if(words(k).length>=10)add(sentences,k,p.id)}
    if(p.quiz){
      quizCount++;
      const q=p.quiz;
      if(!Array.isArray(q)||typeof q[0]!=='string'||!q[0].trim()||!Array.isArray(q[1])||q[1].length<2||q[1].some(a=>typeof a!=='string'||!a.trim())||new Set(q[1].map(norm)).size!==q[1].length||!Number.isInteger(q[2])||q[2]<0||q[2]>=q[1].length||typeof q[3]!=='string'||!q[3].trim())quizIssues.push(p.id);
    }
    vectors.push({id:p.id,g:grams(body(p))});
  }
  for(let i=0;i<vectors.length;i++)for(let j=i+1;j<vectors.length;j++){
    const a=vectors[i],b=vectors[j];let intersection=0;for(const k of a.g)if(b.g.has(k))intersection++;
    const union=a.g.size+b.g.size-intersection,score=union?intersection/union:0;
    if(score>=.12)nearPairs.push({ids:[a.id,b.id],jaccard:Number(score.toFixed(3))});
  }
  return {method:'Whitespace word count; normalized exact sentences of at least 10 words; five-word shingle Jaccard >= 0.12 for manual triage only. No factual or semantic certification.',articles:posts.length,totalWords,minWords:posts.length?minWords:0,maxWords,categories,quizCount,reflectionCount:posts.length-missingReflection.length,missingReflection,reviewMissing,quizIssues,failures,duplicateTitles:duplicates(titles),duplicatePrompts:duplicates(prompts),duplicateSentences:duplicates(sentences),nearPairs:nearPairs.sort((a,b)=>b.jaccard-a.jaccard)};
}
if(process.argv.includes('--self-test')){
  const t='One two three four five six seven eight nine ten eleven.';
  const x={id:1,title:'Title',category:'Learning',summary:'Summary',body:t,extra:t,source:'Example',url:'https://example.com/',reflection:'What changed?',quiz:['Question',['Yes','No'],0,'Explanation'],editorialReview:{status:'source-aligned revision',date:'2026-11-27',scope:'Example'}};
  const r=audit([x,{...x,id:2,quiz:['Question',['Yes','YES'],0,'Explanation'],url:'http://example.com/'}]);assert.equal(r.duplicateSentences.length,1);assert.equal(r.duplicateTitles.length,1);assert.equal(r.duplicatePrompts.length,1);assert.deepEqual(r.quizIssues,[2]);assert.ok(r.failures.some(x=>x.issue==='invalid source URL'));assert.ok(r.nearPairs.length===1);assert.equal(r.reflectionCount,2);assert.equal(audit([{...x,reflection:''}]).reflectionCount,0);console.log('Editorial audit self-test passed.');
}else{
  const posts=vm.runInNewContext(fs.readFileSync('content.js','utf8')+'\nCONTENT',{}, {timeout:10000});
  const r=audit(posts);
  fs.writeFileSync('editorial-audit.json',JSON.stringify(r,null,2)+'\n');
  console.log(JSON.stringify({articles:r.articles,totalWords:r.totalWords,minWords:r.minWords,maxWords:r.maxWords,quizCount:r.quizCount,reflectionCount:r.reflectionCount,missingReflection:r.missingReflection.length,reviewMissing:r.reviewMissing.length,quizIssues:r.quizIssues.length,duplicateTitles:r.duplicateTitles.length,duplicatePrompts:r.duplicatePrompts.length,duplicateSentences:r.duplicateSentences.length,nearPairs:r.nearPairs.length,failures:r.failures.length}));
  assert.equal(r.articles,208);assert.equal(r.quizCount,80);assert.ok(r.reflectionCount>=132);
  for(const key of ['failures','reviewMissing','quizIssues','duplicateTitles','duplicatePrompts'])assert.equal(r[key].length,0,JSON.stringify(r[key]));
}
