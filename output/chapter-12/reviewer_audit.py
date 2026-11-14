"""Independent read-only PDF checks; writes reviewer evidence only."""
from pathlib import Path
import hashlib, json
import pymupdf as fitz
from PIL import Image, ImageChops

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).parent
register=json.loads((ROOT/'production/chapter-reviews.json').read_text(encoding='utf-8-sig'))
folders=['primary-1-opening']+[f'chapter-{i}' for i in range(3,12)]
seen=set(); results=[]
for c in register['chapters'][:12]:
    folder=folders[0] if c['id'] in ('P1-01','P1-02') else f"chapter-{int(c['id'][-2:])}"
    for kind,p in c['artifacts'].items():
        if p in seen: continue
        seen.add(p); pdf=ROOT/p; doc=fitz.open(pdf)
        pages=[]; texts=[]
        for i,page in enumerate(doc):
            pic=page.get_pixmap(matrix=fitz.Matrix(1.15,1.15),alpha=False)
            actual=Image.frombytes('RGB',(pic.width,pic.height),pic.samples)
            png=ROOT/'output'/folder/kind/f'page-{i+1:02}.png'
            prior=Image.open(png).convert('RGB')
            same=actual.size==prior.size and ImageChops.difference(actual,prior).getbbox() is None
            bounds=[]
            for b in page.get_text('blocks'):
                if b[0]<0 or b[1]<0 or b[2]>page.rect.width or b[3]>page.rect.height: bounds.append(b[:4])
            pages.append({'page':i+1,'png':str(png.relative_to(ROOT)).replace('\\','/'),'pixel_match':same,'size':[pic.width,pic.height],'outside_text':bounds})
            texts.append(f'\n--- {kind.upper()} PAGE {i+1} ---\n'+page.get_text())
        stem=folder+'-'+kind
        (OUT/f'reviewer-{stem}-text.txt').write_text(''.join(texts),encoding='utf-8')
        results.append({'pdf':p,'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pages':len(doc),'a4':all(abs(p.rect.width-595.276)<1 and abs(p.rect.height-841.89)<1 for p in doc),'page_checks':pages})
(OUT/'reviewer-final-pdf-checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps({'pdfs':len(results),'pages':sum(r['pages'] for r in results),'pixel_matches':sum(p['pixel_match'] for r in results for p in r['page_checks']),'a4':all(r['a4'] for r in results),'outside_text':sum(len(p['outside_text']) for r in results for p in r['page_checks'])}))
