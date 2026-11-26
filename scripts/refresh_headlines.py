"""Collect only publisher titles and URLs; no article text, secrets or AI."""
import datetime as dt
import email.utils
import json
import pathlib
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

PATH = pathlib.Path(__file__).resolve().parents[1] / "fresh.json"
FEEDS = (
    ("NASA", "https://www.nasa.gov/news-release/feed/"),
    ("Library of Congress", "https://blogs.loc.gov/thesignal/feed/"),
    ("Library of Congress History", "https://blogs.loc.gov/teachers/feed/"),
    ("Smithsonian Science", "https://feeds.feedburner.com/smithsonianmag/science-nature"),
    ("Smithsonian History", "https://feeds.feedburner.com/smithsonianmag/history-archaeology"),
)
HOSTS = {"www.nasa.gov", "science.nasa.gov", "blogs.loc.gov", "www.loc.gov", "www.smithsonianmag.com", "smithsonianmag.com", "www.science.org"}

def trusted(url):
    p = urllib.parse.urlsplit(url)
    return p.scheme == "https" and p.hostname in HOSTS

def get_items(name, url):
    req = urllib.request.Request(url, headers={"User-Agent":"ARETE educational feed reader/0.3"})
    with urllib.request.urlopen(req, timeout=20) as response:
        if not trusted(response.geturl()) and urllib.parse.urlsplit(response.geturl()).hostname not in {"feeds.feedburner.com", "feeds2.feedburner.com"}:
            raise ValueError("Unexpected redirect")
        xml = response.read(2_000_001)
    if len(xml) > 2_000_000:
        raise ValueError("RSS size limit")
    root = ET.fromstring(xml)
    items = []
    for item in root.findall("./channel/item")[:10]:
        title = " ".join((item.findtext("title") or "").split())
        link = (item.findtext("link") or "").strip()
        pub = item.findtext("pubDate") or ""
        try:
            date = email.utils.parsedate_to_datetime(pub).date().isoformat()
        except (ValueError, TypeError, AttributeError):
            date = ""
        if title and len(title) < 500 and trusted(link):
            items.append({"title":title,"url":link,"date":date,"source":name})
    return items

def main():
    old = json.loads(PATH.read_text(encoding="utf-8"))
    current = {}
    success = 0
    for name, url in FEEDS:
        try:
            new = get_items(name, url)
            if not new:
                raise ValueError("Empty feed")
            current[name] = new
            success += 1
        except Exception as exc:
            print(name, type(exc).__name__, str(exc)[:180])
            current[name] = [i for i in old.get("items",[]) if i.get("source")==name and trusted(i.get("url",""))]
    if not success:
        raise SystemExit("All sources failed; keeping previous digest unchanged.")
    merged = {}
    for entries in current.values():
        for item in entries:
            merged[item["url"]] = item
    items = sorted(merged.values(), key=lambda item:item["date"], reverse=True)[:50]
    if items == old.get("items",[]):
        print("No headline changes")
        return
    payload = {"updated":dt.datetime.now(dt.timezone.utc).isoformat(),"items":items}
    PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
    print("Stored",len(items),"publisher links")

if __name__ == "__main__":
    main()
