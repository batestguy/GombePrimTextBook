"""Run only after the legacy validator process has completed successfully."""
import json,shutil,fitz
from pathlib import Path
r=Path(__file__).resolve().parents[2];o=r/'output/chapter-13'
m=json.loads((r/'production/page_manifest.json').read_text())
d=fitz.open(r/'Gombe-Mathematics-Book-1.pdf');s=fitz.open(r/'output/pdf/sample-lessons.pdf');j=0
for label in ['P1-01','P2-04','P3-15']:
 n=next(i for i,p in enumerate(m) if p['label']==label)
 for offset in [0,1]:
  assert s[j].get_text()==d[n+offset].get_text()
  assert s[j].get_pixmap().samples==d[n+offset].get_pixmap().samples
  j+=1
result={'build':'passed','render':'passed','validate':'passed','pages':len(d),'sample_pages_pixel_and_text_equal':j,'validation':json.loads((r/'output/validation.json').read_text())}
d.close();s.close()
backups=json.loads((o/'generated-backups.json').read_text())
for target,source in backups.items():shutil.copyfile(r/source,r/target)
assert all((r/t).read_bytes()==(r/b).read_bytes() for t,b in backups.items())
result['historical_files_exactly_restored']=len(backups)
(o/'legacy-cycle.json').write_text(json.dumps(result,indent=2)+'\n')
print('6 sample pages match;21 historical files exactly restored')
