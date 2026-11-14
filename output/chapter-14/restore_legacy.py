from pathlib import Path
p=Path('scripts/build_chapter_fourteen.py');s=p.read_text();s=s.replace("if x['type']=='s' and abs(x['rect'].height)<.01","if x['type']=='s'");s=s.replace('for e in expected):found.append','for e in expected+ticks):found.append');p.write_text(s)
import json,hashlib,shutil
R=Path.cwd();o=R/'output/chapter-14';backup=json.loads((o/'generated-backups.json').read_text())
# Record ephemeral legacy result, then restore exact historical files.
legacy=json.loads((R/'output/validation.json').read_text());(o/'legacy-validation.json').write_text(json.dumps(legacy,indent=2)+'\n')
for dest,src in backup.items():shutil.copyfile(R/src,R/dest)
assert all((R/a).read_bytes()==(R/b).read_bytes() for a,b in backup.items())
(o/'legacy-restoration.json').write_text(json.dumps({'restored_count':len(backup),'all_byte_identical':True,'commands':['python scripts/build_book.py','quarto render book.qmd','python scripts/validate_book.py'],'legacy_pages':legacy['pages'],'legacy_status':'passed; historical export restored; no redesign approval'},indent=2)+'\n')
