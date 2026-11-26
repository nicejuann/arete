"""Build a validated Protestant WEB offline pack from the official eBible VPL archive."""
import hashlib,io,json,pathlib,re,urllib.request,urllib.parse,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
SOURCE="https://ebible.org/Scriptures/engwebp_vpl.zip"
CODES="GEN EXO LEV NUM DEU JOS JDG RUT 1SA 2SA 1KI 2KI 1CH 2CH EZR NEH EST JOB PSA PRO ECC SNG ISA JER LAM EZK DAN HOS JOL AMO OBA JON MIC NAM HAB ZEP HAG ZEC MAL MAT MRK LUK JHN ACT ROM 1CO 2CO GAL EPH PHP COL 1TH 2TH 1TI 2TI TIT PHM HEB JAS 1PE 2PE 1JN 2JN 3JN JUD REV".split()
COUNTS=[50,40,27,36,34,24,21,4,31,24,22,25,29,36,10,13,10,42,150,31,12,8,66,52,5,48,12,14,3,9,1,4,7,3,3,3,2,14,4,28,16,24,21,28,16,16,13,6,6,4,4,5,3,6,4,3,1,13,5,5,3,5,1,1,1,22]
ALIASES=dict(zip(CODES,CODES))
for code, variants in {"EXO":"EXOD","DEU":"DEUT","JOS":"JOSH","JDG":"JUDG","RUT":"RUTH","1SA":"1SAM","2SA":"2SAM","1KI":"1KGS 1KING","2KI":"2KGS 2KING","1CH":"1CHR","2CH":"2CHR","PSA":"PS PSALM PSALMS","PRO":"PROV","ECC":"ECCL","SNG":"SOL SONG SOS","EZK":"EZE EZEK","JOL":"JOE JOEL","NAM":"NAH","MAT":"MATT","MRK":"MAR MARK","LUK":"LUKE","JHN":"JOH JOHN","1CO":"1COR","2CO":"2COR","PHP":"PHI PHIL","1TH":"1THESS","2TH":"2THESS","1TI":"1TIM","2TI":"2TIM","PHM":"PHLM","1PE":"1PET","2PE":"2PET","1JN":"1JO 1JOHN","2JN":"2JO 2JOHN","3JN":"3JO 3JOHN","JUD":"JUDE","REV":"REVELATION"}.items():
    for variant in variants.split(): ALIASES[variant]=code
def build(raw):
    books={c:[{} for _ in range(n)] for c,n in zip(CODES,COUNTS)}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=[n for n in z.namelist() if n.lower().endswith("_vpl.txt")]
        if len(names)!=1: raise ValueError("Expected exactly one VPL source file")
        if z.getinfo(names[0]).file_size>20000000: raise ValueError("VPL too large")
        text=z.read(names[0]).decode("utf-8-sig")
    for line in text.splitlines():
        m=re.match(r"^\s*([1-3]?[A-Za-z]+)\s+(\d+):(\d+)\s+(.+)$",line)
        if not m: continue
        name,ch,verse,value=m.groups()
        code=ALIASES.get(name.upper())
        if code is None: raise ValueError("Unknown book code "+name)
        ch,verse=int(ch),int(verse)
        if not 1<=ch<=len(books[code]) or not 1<=verse<=176: raise ValueError("Invalid reference")
        chapter=books[code][ch-1]
        if verse in chapter: raise ValueError("Duplicate verse")
        chapter[verse]=value
    ordered=[{"code":c,"chapters":[[{"verse":v,"text":t} for v,t in sorted(ch.items())] for ch in books[c]]} for c in CODES]
    chapters=sum(len(b["chapters"]) for b in ordered)
    count=sum(len(ch) for b in ordered for ch in b["chapters"])
    if len(ordered)!=66 or chapters!=1189 or count<30000 or any(not ch for b in ordered for ch in b["chapters"]):
        raise ValueError(f"Incomplete Scripture pack: {chapters} chapters, {count} verses")
    return {"edition":"engwebp","source":SOURCE,"sourceSha256":hashlib.sha256(raw).hexdigest(),"verseCount":count,"books":ordered}
def main():
    req=urllib.request.Request(SOURCE,headers={"User-Agent":"ARETE/1.2 (https://github.com/nicejuann/arete)"})
    with urllib.request.urlopen(req,timeout=60) as r:
        if urllib.parse.urlsplit(r.geturl()).hostname not in {"ebible.org","www.ebible.org"}: raise ValueError("Unexpected source")
        raw=r.read(15000001)
    if len(raw)>15000000: raise ValueError("Archive too large")
    pack=build(raw)
    (ROOT/"bible-webp.json").write_text(json.dumps(pack,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
    print("Validated 66 books, 1189 chapters,",pack["verseCount"],"verses")
if __name__=="__main__": main()
