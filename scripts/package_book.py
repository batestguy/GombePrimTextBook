"""Package only explicit publication-source directories; exclude caches and temporary files."""
from pathlib import Path
import json,zipfile,hashlib,shutil
R=Path(__file__).resolve().parent.parent
out=R/'output'
shutil.copy2(R/'Gombe-Mathematics-Book-1.pdf',out/'pdf/Gombe-Mathematics-Book-1.pdf')
manifest=json.loads((R/'production/page_manifest.json').read_text(encoding='utf-8'))
labels=[p['label'] for p in manifest]
groups={
'Front matter, photograph, contents and class journeys':sum(x in ['cover','welcome','how','friends','gombe-photo','contents','journey1','journey2','journey3'] for x in labels),
'Class openers':3,'Lesson pages':126,'Revision and assessment pages':15,'Multiplication reference':1,'AI teaching pages':4,'Teacher guidance':8,'Lesson answer pages':32,'Revision/assessment answer pages':5,'AI answer page':1,'Supplementary teacher checks':15,'Curriculum evidence and crosswalk':24,'Glossary':2,'Credits':1,'Book 2 preview':1}
assert sum(groups.values())==247
budget='# Contents and page budget\n\nFinal digital review allocation; there was no fixed page cap. Term groupings are editorial, not an official scheme.\n\n| Section | Pages |\n|---|---:|\n'+'\n'.join(f'| {k} | {v} |' for k,v in groups.items())+'\n| **Total** | **247** |\n\n'
budget+='| Book page | Stable page ID |\n|---:|---|\n'+'\n'.join(f'| {p["page"]} | {p["label"]} |' for p in manifest)+'\n'
(R/'production/contents-and-page-budget.md').write_text(budget,encoding='utf-8')
files=[R/p for p in ['README.md','AGENTS.md','GombeTextbook.txt','_quarto.yml','book.qmd','book.typ','requirements-validation.txt']]
for dirname in ['production','research','artwork','fonts','scripts']:
 files += [p for p in (R/dirname).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc']
files += [out/'VALIDATION.md',out/'validation.json',out/'arithmetic_checks.json',out/'pdf/sample-lessons.pdf',out/'pdf/Gombe-Mathematics-Book-1.pdf']
files += sorted((out/'page-review').glob('contact-*.png'))
records=[{'file':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(set(files))]
(out/'DELIVERY-MANIFEST.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
files.append(out/'DELIVERY-MANIFEST.json')
target=out/'Gombe-Mathematics-Book-1-editable.zip'
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(set(files)):z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(target) as z:
 assert z.testzip() is None
 assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist())
 assert 'artwork/characters.png' in z.namelist() and 'fonts/LICENSE_DEJAVU.txt' in z.namelist()
 destination=R/'tmp/rebuild-check'
 destination.mkdir(parents=True,exist_ok=True)
 z.extractall(destination)
print(json.dumps({'archive':str(target.relative_to(R)),'files':len(set(files)),'archive_bytes':target.stat().st_size,'pdf_bytes':(out/'pdf/Gombe-Mathematics-Book-1.pdf').stat().st_size,'zip_crc':'passed','source_extract':'tmp/rebuild-check'},indent=2))
