from pathlib import Path
import json,hashlib,sys,importlib.metadata,shutil
R=Path(__file__).resolve().parent.parent
assets=[]
ids={'characters':'exec-be79dcd0-f669-47fe-b26f-6818a566ca0c','school':'exec-4a245050-74a4-4194-bc7e-2b8a7be56339','market':'exec-47f9c153-c5f7-4f0c-8fc8-1f760c104c03','garden':'exec-dcbb7170-cf7d-45c3-896a-1bfbd8948e4a'}
prompts={
'characters':'Four full-body fictional Nigerian school friends on cream: Amina mustard headscarf teal dress; Musa blue shirt brown trousers; Zainab two braids coral blouse navy skirt; Daniel green shirt grey trousers and wheelchair. Warm watercolour/coloured pencil, no lettering or logos.',
'school':'Canonical friends with female teacher at accessible low school table, reusable tops, exercise books, string, containers, school veranda and garden. Keep faces and clothes from character reference. No assessed quantities, writing or landmarks.',
'market':'Canonical friends and supervising adult at a shaded produce stall, baskets, grain sacks and accessible path. Everyday northern Nigerian town. No prices, numbers, text, landmarks or logos; decorative quantities only.',
'garden':'Canonical friends and teacher in school garden measuring with string, ruler and safe jug, accessible paths. No quantitative labels or identifiable landmark; decorative scene.'}
for name,gid in ids.items():
 p=R/'artwork'/f'{name}.png'
 assets.append(dict(file=str(p.relative_to(R)).replace('\\','/'),type='original AI-assisted illustration',provider='OpenAI built-in image generation tool',date='2026-10-17',generation_id=gid,prompt_record='Concise reconstruction of generation instructions; canonical style in STYLE.md',prompt=prompts[name],reference='characters.png' if name!='characters' else None,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rights_note='No external photographer or source character; publisher to review AI-assisted artwork rights. No claim of human authorship or guaranteed exclusivity.'))
p=R/'artwork/kilang-hill.jpg'
assert hashlib.sha1(p.read_bytes()).hexdigest()=='40295b73b4a6e4a2c5737ae19ff26bf387a7803e'
assets.append(dict(file='artwork/kilang-hill.jpg',type='selected photograph',title='Kilang Hill',creator='Huzaifakumo',date='2022-10-15',source='https://commons.wikimedia.org/wiki/File:Kilang_Hill.jpg',original_url='https://upload.wikimedia.org/wikipedia/commons/b/bc/Kilang_Hill.jpg',source_revision='https://commons.wikimedia.org/w/index.php?title=File:Kilang_Hill.jpg&oldid=1055444140',location_evidence='Photographer description: Kilang Hill in Kaltungo LGA; no independent field/GPS verification claimed.',licence='CC BY-SA 4.0',licence_url='https://creativecommons.org/licenses/by-sa/4.0/',changes='None; proportional uncropped page placement only.',sha1=hashlib.sha1(p.read_bytes()).hexdigest(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),permission_basis='Public licence on author’s own-work upload; source and licence attribution beside image. No endorsement implied.'))
assets.append(dict(file='artwork/diagrams/*.svg',type='deterministic vector mathematics artwork',creator='Project code, scripts/make_diagrams.py',quantity_manifest='artwork/diagrams/manifest.json',rights_note='Original project diagrams; mathematical quantities controlled by code.'))
(R/'artwork/PROVENANCE.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2),encoding='utf-8')
env={'python':sys.version,'quarto':'1.9.38','typst':'0.14.2','packages':{n:importlib.metadata.version(n) for n in ['PyMuPDF','Pillow']},'platform':'Windows','network_required_for_render':False}
(R/'production/environment.json').write_text(json.dumps(env,indent=2),encoding='utf-8')
(R/'requirements-validation.txt').write_text('\n'.join(n+'=='+v for n,v in env['packages'].items())+'\n',encoding='utf-8')
print('Recorded 4 original illustrations, 1 licensed photograph, 17 vector diagrams and environment versions.')
