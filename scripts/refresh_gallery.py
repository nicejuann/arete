"""Acquire only CC0 public-domain art records from The Met's open API."""
import datetime as dt
import json
import pathlib
import sys
import urllib.parse as up
import urllib.request as ur
ROOT=pathlib.Path(__file__).resolve().parents[1]
PATH=ROOT/"gallery.json"
API="https://collectionapi.metmuseum.org/public/collection/v1"
THEMES=("Japanese woodblock print","landscape painting","ancient Egyptian sculpture","ceramic vessel","illuminated manuscript","architectural drawing","textile","ancient Greek pottery","botanical illustration","portrait painting")
CC0="https://creativecommons.org/publicdomain/zero/1.0/"
def get_json(path):
    req=ur.Request(API+path,headers={"User-Agent":"ARETE-Gallery/0.9 (https://github.com/nicejuann/arete)"})
    with ur.urlopen(req,timeout=15) as r:
        if up.urlsplit(r.geturl()).hostname!="collectionapi.metmuseum.org":
            raise ValueError("Unexpected redirect")
        data=r.read(2000001)
    if len(data)>2000000:
        raise ValueError("Response too large")
    return json.loads(data)
def valid_url(url,hosts):
    try:
        u=up.urlsplit(url)
        return u.scheme=="https" and u.hostname in hosts and not u.username and not u.password
    except (TypeError,ValueError):
        return False
def normalize(o):
    if o.get("isPublicDomain") is not True:
        return None
    pid=o.get("objectID")
    image=o.get("primaryImageSmall") or o.get("primaryImage")
    url=o.get("objectURL")
    if not isinstance(pid,int) or pid<=0 or not valid_url(image,{"images.metmuseum.org"}) or not valid_url(url,{"www.metmuseum.org","metmuseum.org"}):
        return None
    if up.urlsplit(url).path.rstrip("/")!="/art/collection/search/"+str(pid):
        return None
    def field(key,limit):
        s=o.get(key,"")
        return " ".join(s.split())[:limit] if isinstance(s,str) else ""
    title=field("title",200)
    if not title:
        return None
    return {"id":"met-"+str(pid),"title":title,"artist":field("artistDisplayName",140),"date":field("objectDate",100),"culture":field("culture",100),"medium":field("medium",180),"credit":field("creditLine",300),"image":image,"url":url,"license":"CC0","licenseUrl":CC0,"source":"The Metropolitan Museum of Art","retrieved":dt.datetime.now(dt.timezone.utc).date().isoformat()}
def collect():
    old=json.loads(PATH.read_text(encoding="utf-8"))
    merged={p["id"]:p for p in old.get("items",[]) if isinstance(p,dict) and p.get("id")}
    today=dt.datetime.now(dt.timezone.utc).date()
    fresh=[]
    for i in range(3):
        theme=THEMES[(today.toordinal()*3+i)%len(THEMES)]
        try:
            found=get_json("/search?"+up.urlencode({"q":theme,"hasImages":"true","isPublicDomain":"true"}))
            ids=list(dict.fromkeys(n for n in (found.get("objectIDs") or []) if isinstance(n,int)))
            if not ids:
                continue
            offset=(today.toordinal()*7)%len(ids)
            accepted=0
            for pid in (ids[offset:]+ids[:offset])[:6]:
                if "met-"+str(pid) in merged:
                    continue
                try:
                    p=normalize(get_json("/objects/"+str(pid)))
                except Exception as exc:
                    print("Object unavailable",pid,str(exc)[:120])
                    continue
                if p:
                    merged[p["id"]]=p
                    fresh.append(p)
                    accepted+=1
                if accepted>=2:
                    break
        except Exception as exc:
            print("Theme unavailable",theme,str(exc)[:120])
    if not fresh:
        print("No new qualifying artworks; previous collection retained")
        return
    items=sorted(merged.values(),key=lambda p:(p["retrieved"],p["id"]),reverse=True)[:120]
    PATH.write_text(json.dumps({"updated":dt.datetime.now(dt.timezone.utc).isoformat(),"items":items},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("New CC0 records",len(fresh),"total",len(items))
def self_test():
    o={"objectID":123,"isPublicDomain":True,"primaryImageSmall":"https://images.metmuseum.org/example.jpg","objectURL":"https://www.metmuseum.org/art/collection/search/123","title":"Example"}
    assert normalize(o)["id"]=="met-123"
    assert normalize({**o,"isPublicDomain":False}) is None
    assert normalize({**o,"primaryImageSmall":"https://example.org/test.jpg"}) is None
    assert normalize({**o,"objectURL":"https://www.metmuseum.org/art/collection/search/456"}) is None
    print("Gallery fixture tests passed")
if __name__=="__main__":
    self_test() if "--test" in sys.argv else collect()
