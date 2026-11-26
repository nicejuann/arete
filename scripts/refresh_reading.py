"""Fetch plain-text excerpts from a fixed list of educational Wikipedia topics.

Only CC BY-SA 4.0 text; no images, quotes selected from separate sources, or user data.
Output excerpts are unreviewed, not ARETE-authored. Attribution and revision links
travel with every item. A source page may have additional attribution notices.
"""
import datetime as dt
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / "open-reading.json"
TOPICS = json.loads((ROOT / "scripts" / "reading-topics.json").read_text(encoding="utf-8"))
API = "https://en.wikipedia.org/w/api.php"
LICENSE = "https://creativecommons.org/licenses/by-sa/4.0/"
MAX_ITEMS = 100

def fetch(params):
    url = API + "?" + urllib.parse.urlencode({"action":"query","format":"json","formatversion":"2", **params})
    req = urllib.request.Request(url, headers={"User-Agent":"ARETE-Reading/0.8 (https://github.com/nicejuann/arete; educational public-domain and open-license reader)"})
    with urllib.request.urlopen(req, timeout=30) as response:
        if urllib.parse.urlsplit(response.geturl()).hostname != "en.wikipedia.org":
            raise ValueError("Unexpected redirect")
        data = response.read(3_000_001)
    if len(data) > 3_000_000:
        raise ValueError("API response exceeded size limit")
    obj = json.loads(data)
    if "error" in obj:
        raise ValueError(str(obj["error"])[:180])
    return obj.get("query", {})

def excerpt(raw):
    text = raw.strip()
    # Keep complete paragraphs where possible. Never add wording or rewrite claims.
    blocks = [b.strip() for b in re.split(r"\n\s*\n|\n", text) if b.strip()]
    out = ""
    for block in blocks:
        candidate = (out + "\n\n" + block).strip()
        if len(candidate) <= 2600:
            out = candidate
        else:
            break
    if len(out.split()) < 100:
        piece = text[:2600]
        ends = [m.end() for m in re.finditer(r"[.!?](?=\s|$)", piece)]
        out = piece[:ends[-1]].strip() if ends else ""
    if not (100 <= len(out.split()) <= 550) or len(out) > 2600:
        return ""
    return out

def normalize(page, category, requested_title):
    if page.get("missing") or page.get("ns") != 0 or "disambiguation" in page.get("pageprops", {}):
        return None
    if page.get("title") != requested_title:
        return None  # avoid unexpected redirects
    text = excerpt(page.get("extract", ""))
    rev = page.get("lastrevid")
    pid = page.get("pageid")
    if not text or not isinstance(rev, int) or not isinstance(pid, int) or pid <= 0 or rev <= 0:
        return None
    title = page["title"]
    if len(title) > 160:
        return None
    url = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"), safe="")
    return {"id":"wiki-"+str(pid),"title":title,"category":category,"text":text,
            "source":"English Wikipedia contributors","url":url,
            "revision":"https://en.wikipedia.org/w/index.php?oldid="+str(rev),
            "history":"https://en.wikipedia.org/w/index.php?title="+urllib.parse.quote(title.replace(" ", "_"),safe="")+"&action=history",
            "license":"CC BY-SA 4.0","licenseUrl":LICENSE,
            "modified":"Lead excerpt; plain text, shortened; not independently reviewed",
            "retrieved":dt.date.today().isoformat()}

def selected_topics(today):
    # Two entries from each category each day, advancing deterministically.
    result = []
    offset = today.toordinal()*2
    for cat, names in TOPICS.items():
        for i in range(min(2,len(names))):
            result.append((cat,names[(offset+i)%len(names)]))
    return result

def collect():
    rights = fetch({"meta":"siteinfo","siprop":"rightsinfo"}).get("rightsinfo", {})
    if "/licenses/by-sa/4.0" not in rights.get("url", ""):
        raise ValueError("Expected site license not confirmed; no publication")
    old = json.loads(PATH.read_text(encoding="utf-8"))
    picked = selected_topics(dt.datetime.now(dt.timezone.utc).date())
    requested = {title:cat for cat,title in picked}
    fresh = []
    # A bounded batch of at most 8 leads per request.
    for i in range(0,len(picked),8):
        titles = [t for _,t in picked[i:i+8]]
        try:
            query = fetch({"prop":"extracts|info|pageprops","exintro":"1","explaintext":"1","exlimit":"max",
                           "titles":"|".join(titles),"ppprop":"disambiguation"})
        except Exception as exc:
            print("Batch unavailable",str(exc)[:180])
            continue
        for page in query.get("pages", []):
            title = page.get("title")
            if title not in requested:
                continue
            item = normalize(page,requested[title],title)
            if item:
                fresh.append(item)
    if not fresh:
        raise SystemExit("No qualifying excerpts. Previous collection retained.")
    merged = {p["id"]:p for p in old.get("items",[]) if isinstance(p,dict) and p.get("id")}
    for p in fresh:
        merged[p["id"]] = p
    # Prefer freshly retrieved entries and keep a bounded archive.
    items = sorted(merged.values(),key=lambda p:(p.get("retrieved",""),p["id"]),reverse=True)[:MAX_ITEMS]
    payload = {"updated":dt.datetime.now(dt.timezone.utc).isoformat(),"items":items}
    PATH.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Imported",len(fresh),"qualifying excerpts; collection now",len(items))

def self_test():
    raw = ("A sample educational sentence describes a familiar natural process. " * 14).strip()
    page = {"ns":0,"title":"Sample","pageid":123,"lastrevid":456,"extract":raw}
    item = normalize(page,"Science","Sample")
    assert item and item["id"]=="wiki-123" and item["revision"].endswith("456")
    assert item["licenseUrl"]==LICENSE and len(item["text"].split())>=100
    assert normalize({**page,"pageprops":{"disambiguation":""}},"Science","Sample") is None
    assert normalize({**page,"title":"Unexpected"},"Science","Sample") is None
    assert normalize({**page,"extract":"Too short."},"Science","Sample") is None
    assert len(selected_topics(dt.date(2026,11,26)))==16
    print("Open reading fixture tests passed")

if __name__ == "__main__":
    if "--test" in sys.argv:
        self_test()
    else:
        collect()
