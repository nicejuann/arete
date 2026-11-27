"""Structured public source check. Network success does not establish factual accuracy."""
import concurrent.futures as cf
import datetime as dt
import json
import pathlib
import threading
import csv
from collections import Counter
from collections import defaultdict, deque
HOST_LIMITS=defaultdict(lambda: threading.BoundedSemaphore(2))
import urllib.error as ue
import urllib.request as ur
import urllib.parse as up
ROOT=pathlib.Path(__file__).resolve().parents[1]
def attempt(url, ranged):
    headers={"User-Agent":"ARETE-Link-Audit/1.1 (https://github.com/nicejuann/arete)"}
    if ranged: headers["Range"]="bytes=0-1023"
    try:
        with ur.urlopen(ur.Request(url,headers=headers),timeout=10) as response:
            status=response.status
            return {"status":status,"result":"reachable" if 200<=status<300 else "unverified","final":response.geturl(),"content_type":response.headers.get("Content-Type","")}
    except ue.HTTPError as exc:
        return {"status":exc.code,"result":"unavailable" if exc.code in (404,410) else "unverified"}
    except Exception as exc:
        return {"result":"unverified","reason":type(exc).__name__}
def check(record):
    url=record["url"]
    host=up.urlsplit(url).hostname
    with HOST_LIMITS[host]:
        result=attempt(url,True)
        # Do not immediately repeat an access-denied or rate-limited request.
        if result.get("status") in (400,405,416):
            result=attempt(url,False)
    if result["result"]=="reachable":
        media={r["role"] for r in record["refs"]}
        mime=result.get("content_type","").lower()
        if "image" in media and mime and not mime.startswith("image/") and "octet-stream" not in mime:
            result["result"]="unverified";result["reason"]="image content type mismatch"
        if "video file" in media and mime and not mime.startswith("video/") and "octet-stream" not in mime:
            result["result"]="unverified";result["reason"]="video content type mismatch"
        if "audio file" in media and mime and not mime.startswith("audio/") and "octet-stream" not in mime:
            result["result"]="unverified";result["reason"]="audio content type mismatch"
    return {**record,**result}
def diagnostic_reason(item):
    if item["result"]=="reachable":return "reachable"
    status=item.get("status")
    reason=item.get("reason")
    if reason and "content type mismatch" in reason:return reason
    if status in (404,410):return "HTTP missing or gone"
    if status in (401,403,451):return "HTTP access restricted"
    if status==429:return "HTTP rate limited"
    if isinstance(status,int) and status>=500:return "HTTP server error"
    if isinstance(status,int) and status>=400:return "HTTP other client error"
    if reason:return "Network or transport: "+str(reason)
    return "Unexpected or unclassified response"
def diagnostic_rows(items):
    rows=[]
    for item in items:
        if item["result"]=="reachable":continue
        refs=item.get("refs",[])
        rows.append({
            "url":item["url"],"host":up.urlsplit(item["url"]).hostname or "",
            "result":item["result"],"status":item.get("status"),"reason":diagnostic_reason(item),
            "roles":sorted({r["role"] for r in refs}),
            "article_ids":sorted({int(r["id"]) for r in refs if r.get("role") in {"original source","image","image credit","media source","video file"} and str(r.get("id","")).isdigit()}),
            "references":refs
        })
    return sorted(rows,key=lambda r:(r["result"]!="unavailable",r["host"],r["url"]))
def diagnostic_summary(rows):
    return {"by_reason":dict(sorted(Counter(r["reason"] for r in rows).items())),
            "by_host":dict(sorted(Counter(r["host"] for r in rows).items())),
            "affected_original_articles":len({i for r in rows for i in r["article_ids"]}),
            "unresolved_count":len(rows)}
def rotate(rows,limit,week):
    if limit<=0:return []
    if len(rows)<=limit:return rows[:]
    offset=(week*limit)%len(rows)
    return (rows[offset:]+rows[:offset])[:limit]
def choose_records(records,week,budget=200):
    # Reserve coverage for app/media files and imported collections, not only original references.
    primary=[r for r in records if any(x["role"] in {"original source","image","video file","media source"} for x in r["refs"])]
    direct=[r for r in records if r not in primary and any(x["role"]=="audio file" for x in r["refs"])]
    other=[r for r in records if r not in primary and r not in direct]
    a=rotate(primary,min(len(primary),int(budget*.75)),week)
    b=rotate(direct,min(len(direct),max(0,budget-len(a))),week)
    c=rotate(other,max(0,budget-len(a)-len(b)),week)
    chosen=a+b+c
    if len(chosen)<budget:
        chosen+=rotate([r for r in records if r not in chosen],budget-len(chosen),week)
    # Interleave hosts to avoid queueing many consecutive calls to one publisher.
    buckets=defaultdict(deque)
    for r in chosen:buckets[up.urlsplit(r["url"]).hostname].append(r)
    ordered=[]
    while any(buckets.values()):
        for queue in buckets.values():
            if queue:ordered.append(queue.popleft())
    return ordered
def self_test():
    def record(i,role):return {"url":f"https://example{i%5}.test/{i}","refs":[{"role":role}]}
    rows=[record(i,"original source") for i in range(250)]+[record(i,"audio file") for i in range(250,258)]+[record(i,"headline") for i in range(258,330)]
    first=choose_records(rows,10);second=choose_records(rows,11)
    assert len(first)==200 and len({r["url"] for r in first})==200
    assert sum(r["refs"][0]["role"]=="audio file" for r in first)==8
    assert sum(r["refs"][0]["role"]=="headline" for r in first)>0
    assert {r["url"] for r in first}!={r["url"] for r in second}
    assert len(choose_records(rows[:3],10))==3
    full=choose_records(rows,10,len(rows))
    assert len(full)==len(rows) and {r['url'] for r in full}=={r['url'] for r in rows}
    assert len({r['url'] for r in full})==len(full)
    print("Audit sampling: coverage, unique links, rotation, small inventory and full coverage passed")
    fixtures=[
        {"url":"https://example.test/a","result":"unverified","status":403,"refs":[{"role":"original source","id":"12"},{"role":"original source","id":"12"}]},
        {"url":"https://example.test/b","result":"unavailable","status":404,"refs":[{"role":"image","id":"13"}]},
        {"url":"https://other.test/c","result":"unverified","status":200,"reason":"audio content type mismatch","refs":[{"role":"audio file","id":""}]},
        {"url":"https://other.test/d","result":"reachable","status":200,"refs":[]},
        {"url":"https://other.test/e","result":"unverified","status":429,"refs":[]},
        {"url":"https://other.test/f","result":"unverified","reason":"TimeoutError","refs":[]},
        {"url":"https://other.test/g","result":"unverified","status":503,"refs":[]}
    ]
    diag=diagnostic_rows(fixtures)
    totals=diagnostic_summary(diag)
    assert len(diag)==6 and diag[0]["result"]=="unavailable"
    assert totals["affected_original_articles"]==2 and totals["by_host"]=={"example.test":2,"other.test":4}
    assert totals["by_reason"]["HTTP access restricted"]==1
    assert totals["by_reason"]["HTTP rate limited"]==1
    assert totals["by_reason"]["HTTP server error"]==1
    assert totals["by_reason"]["audio content type mismatch"]==1
    assert totals["by_reason"]["Network or transport: TimeoutError"]==1
    assert totals["by_reason"]["HTTP missing or gone"]==1
    assert sum(totals["by_reason"].values())==totals["unresolved_count"]
    print("Audit diagnostics: reason classification, host aggregation, affected article deduplication and reachable exclusion passed")
def main(full=False):
    data=json.loads((ROOT/"source-inventory.json").read_text(encoding="utf-8"))
    records=[r for r in data["links"] if up.urlsplit(r["url"]).hostname not in {"raw.githubusercontent.com","github.com","bible-api.com"}]
    chosen=choose_records(records,dt.date.today().toordinal()//7,len(records) if full else 200)
    if full and (len(chosen)!=len(records) or len({r['url'] for r in chosen})!=len(records)):
        raise RuntimeError('Full audit did not cover every eligible unique URL')
    with cf.ThreadPoolExecutor(max_workers=8) as pool: items=list(pool.map(check,chosen))
    summary={k:sum(x["result"]==k for x in items) for k in ("reachable","unavailable","unverified")}
    (ROOT/"link-audit.json").write_text(json.dumps({"checked_at":dt.datetime.now(dt.timezone.utc).isoformat(),"eligible":len(records),"checked":len(items),"summary":summary,"links":items},indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"eligible":len(records),"checked":len(items),**summary}))
    diagnostics=diagnostic_rows(items)
    totals=diagnostic_summary(diagnostics)
    assert totals["unresolved_count"]==summary["unavailable"]+summary["unverified"]
    (ROOT/"link-diagnostics.json").write_text(json.dumps({"summary":totals,"links":diagnostics},indent=2)+"\n",encoding="utf-8")
    columns=["url","host","result","status","reason","roles","article_ids"]
    with (ROOT/"link-diagnostics.csv").open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=columns)
        writer.writeheader()
        for row in diagnostics:
            writer.writerow({k:json.dumps(row[k]) if isinstance(row[k],list) else row[k] for k in columns})
    print("AUDIT_DIAGNOSTICS "+json.dumps(totals,sort_keys=True))
    for row in diagnostics:
        print("AUDIT_UNRESOLVED "+json.dumps({k:row[k] for k in columns},ensure_ascii=True))
if __name__=="__main__":
    import sys
    if "--self-test" in sys.argv:self_test()
    else:main(full='--all' in sys.argv)
