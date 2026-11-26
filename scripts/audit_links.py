"""Structured public source check. Network success does not establish factual accuracy."""
import concurrent.futures as cf
import datetime as dt
import json
import pathlib
import threading
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
    print("Audit sampling: coverage, unique links, rotation and small inventory passed")
def main():
    data=json.loads((ROOT/"source-inventory.json").read_text(encoding="utf-8"))
    records=[r for r in data["links"] if up.urlsplit(r["url"]).hostname not in {"raw.githubusercontent.com","github.com","bible-api.com"}]
    chosen=choose_records(records,dt.date.today().toordinal()//7)
    with cf.ThreadPoolExecutor(max_workers=8) as pool: items=list(pool.map(check,chosen))
    summary={k:sum(x["result"]==k for x in items) for k in ("reachable","unavailable","unverified")}
    (ROOT/"link-audit.json").write_text(json.dumps({"checked_at":dt.datetime.now(dt.timezone.utc).isoformat(),"eligible":len(records),"checked":len(items),"summary":summary,"links":items},indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"eligible":len(records),"checked":len(items),**summary}))
if __name__=="__main__":
    import sys
    if "--self-test" in sys.argv:self_test()
    else:main()
