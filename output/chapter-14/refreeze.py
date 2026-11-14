from pathlib import Path
import json,hashlib
R=Path.cwd();O=R/'output/chapter-14';old=json.loads((O/'before-rubric-correction-inspection.json').read_text());fp='e79d0c9769260831ed651e970bc4534fc04c5aa23ecbc8983b06447b9e2e4c87'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
changed={};ins={}
for role,rows in old.items():
 changed[role]=[];ins[role]=[]
 for row in rows:
  p=O/role/f"page-{row['page']:02}.png";new=h(p);diff=new!=row['sha256']
  if diff:changed[role].append(row['page'])
  ins[role].append(dict(page=row['page'],sha256=new,result='changed adult page visually re-inspected after rubric correction; readable; no overlap/clipping' if diff else 'unchanged pixel hash; earlier author visual inspection retained'))
assert changed=={'textbook':[14,15,16,17],'workbook':[]},changed
(O/'page-inspection.json').write_text(json.dumps(ins,indent=2)+'\n')
f=json.loads((O/'author-freeze.json').read_text());f['fingerprint']=fp
f['source_hashes']={p:h(R/p) for p in f['source_hashes']}
for role in f['artifacts']:f['artifacts'][role]['sha256']=h(R/f['artifacts'][role]['path'])
f['correction_round']=dict(required_findings='Task-specific six LOCAL rubrics;GUIDED-COMPARE metadata dialogue synchronized',changed_pages=changed,inspection='all4 changed textbook pages visually inspected;27 identical page hashes retain prior inspection',validation='pair builder,canonical lessons regeneration,21historical file exact restoration,preflight,draft gate passed')
(O/'author-freeze.json').write_text(json.dumps(f,indent=2)+'\n')
p=O/'HANDOFF.md';s=p.read_text(encoding='utf-8-sig').replace('948a6032161239a797bf5e0b52747e694c742975b11fca1b0e9b910fe0931a61',fp);s+='\n## Independent-review correction and new freeze\n\nReplaced six LOCAL answer rubrics with only the actions each prompt requests, in canonical task metadata and adult pages. Synchronized GUIDED-COMPARE task metadata to rendered C-is-longest-because-lowest dialogue. Regenerated pair/task coverage/objective matrix/diagram ledger and production/lessons.json. Changed exact PNG pages: TB14,15,16,17; personally re-inspected all4 at readable size: no clipping/overlap. All other27 page hashes match prior inspected pages; workbook PDF hash unchanged. All21 historical generated files restored byte-identically after lessons build. Pair build, preflight and draft gate passed again. The original successful legacy render/validation remains recorded; this correction did not rerun the legacy render/validation, because it changes paired metadata/adult answers only. New fingerprint: '+fp+'. Independent recheck/sign-off pending.\n';p.write_text(s,encoding='utf-8')
with (O/'AUTHOR-PROGRESS.md').open('a',encoding='utf-8') as z:z.write('\n- Correction rebuild passed; regenerated current lessons and restored21historical files exact. Changed TB14-17 re-inspected;27 other page hashes unchanged. Preflight/draft gate passed; new freeze '+fp+'; pending reviewer recheck.\n')
print(json.dumps(changed))
