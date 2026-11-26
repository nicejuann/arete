"""Bounded public source URL audit. No automatic deletion."""
import concurrent.futures as cf
import datetime as dt
import json
import pathlib
import re
import urllib.error as ue
import urllib.parse as up
import urllib.request as ur
ROOT=pathlib.Path(__file__).resolve().parents[1]
def urls():
    result=set()
    for name in ("content.js","app.js","fresh.json","open-reading.json","gallery.json"):
        text=(ROOT/name).read_text(encoding="utf-8")
        for raw in re.findall(r'https://[^ \t\r\n"\'<>\\]+',text):
            u=raw.rstrip(");,]")
            p=up.urlsplit(u)
            if p.scheme=="https" and p.hostname and "." in p.hostname and not p.username and not p.password and not re.search(r"[$\{\}]",u):
                if p.hostname not in {"raw.githubusercontent.com","github.com","bible-api.com"}:
                    result.add(u)
    return sorted(result)
def check(url):
    req=ur.Request(url,headers={"User-Agent":"ARETE-Link-Audit/1.0 (https://github.com/nicejuann/arete)","Range":"bytes=0-1023"})
    try:
        with ur.urlopen(req,timeout=12) as response:
            status=response.status
            return {"url":url,"status":status,"result":"reachable" if 200<=status<300 else "unverified","final":response.geturl()}
    except ue.HTTPError as exc:
        return {"url":url,"status":exc.code,"result":"unavailable" if exc.code in (404,410) else "unverified"}
    except Exception as exc:
        return {"url":url,"result":"unverified","reason":type(exc).__name__}
def main():
    links=urls()
    n=200
    if len(links)>n:
        offset=(dt.date.today().toordinal()//7*n)%len(links)
        links=(links[offset:]+links[:offset])[:n]
    with cf.ThreadPoolExecutor(max_workers=6) as pool:
        items=list(pool.map(check,links))
    summary={k:sum(x["result"]==k for x in items) for k in ("reachable","unavailable","unverified")}
    (ROOT/"link-audit.json").write_text(json.dumps({"checked_at":dt.datetime.now(dt.timezone.utc).isoformat(),"checked":len(items),"summary":summary,"links":items},indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary))
if __name__=="__main__":
    main()
