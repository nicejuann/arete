"""Structured public source check. Network success does not establish factual accuracy."""
import concurrent.futures as cf
import datetime as dt
import json
import pathlib
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
    result=attempt(url,True)
    if result.get("status") in (400,403,405,416):
        result=attempt(url,False)
    if result["result"]=="reachable":
        media={r["role"] for r in record["refs"]}
        mime=result.get("content_type","").lower()
        if "image" in media and mime and not mime.startswith("image/") and "octet-stream" not in mime:
            result["result"]="unverified";result["reason"]="image content type mismatch"
        if "video file" in media and mime and not mime.startswith("video/") and "octet-stream" not in mime:
            result["result"]="unverified";result["reason"]="video content type mismatch"
    return {**record,**result}
def main():
    data=json.loads((ROOT/"source-inventory.json").read_text(encoding="utf-8"))
    records=[r for r in data["links"] if up.urlsplit(r["url"]).hostname not in {"raw.githubusercontent.com","github.com","bible-api.com"}]
    # Always report coverage. Prioritize original sources and media; rotate the rest.
    priority=[r for r in records if any(x["role"] in {"original source","image","video file","media source"} for x in r["refs"])]
    rest=[r for r in records if r not in priority]
    n=200
    def rotate(rows,limit):
        if len(rows)<=limit:return rows
        offset=(dt.date.today().toordinal()//7*limit)%len(rows)
        return (rows[offset:]+rows[:offset])[:limit]
    chosen=rotate(priority,n)
    chosen+=rotate(rest,max(0,n-len(chosen)))
    with cf.ThreadPoolExecutor(max_workers=8) as pool: items=list(pool.map(check,chosen))
    summary={k:sum(x["result"]==k for x in items) for k in ("reachable","unavailable","unverified")}
    (ROOT/"link-audit.json").write_text(json.dumps({"checked_at":dt.datetime.now(dt.timezone.utc).isoformat(),"eligible":len(records),"checked":len(items),"summary":summary,"links":items},indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"eligible":len(records),"checked":len(items),**summary}))
if __name__=="__main__":main()
