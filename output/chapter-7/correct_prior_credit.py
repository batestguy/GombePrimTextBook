"""Authorized one-credit correction, with original P1-06 artifacts archived."""
import sys,json,hashlib,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from build_chapter_five import BundleRenderer
from build_chapter_six import OUT,FILES
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
archive=ROOT/'output/chapter-7/prior-chapter-6';archive.mkdir(exist_ok=True)
baseline=json.loads((ROOT/'output/chapter-7/before.json').read_text())
before_rasters={str(p.relative_to(ROOT)):sha(p) for r in ('textbook','workbook') for p in (OUT/r).glob('page-*.png')}
assert sha(FILES['textbook'])==baseline['hashes'][str(FILES['textbook'].relative_to(ROOT)).replace('\\','/')]
for p in [FILES['textbook'],OUT/'textbook/page-21.png',OUT/'textbook/validation.json']:
 shutil.copy2(p,archive/p.name)
(archive/'before-raster-hashes.json').write_text(json.dumps(before_rasters,indent=2)+'\n')
p=json.loads((ROOT/'production/p1.json').read_text(encoding='utf-8'));lesson=p[5]
credit=lesson['paired_edition']['textbook_pages'][20]['elements'][2]
assert 'provenance artwork/PROVENANCE.json.' in credit['text']
credit['text']=credit['text'].replace('provenance artwork/PROVENANCE.json.','provenance artwork/manifest.json and the matching .provenance.json sidecar.')
(ROOT/'production/p1.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
reports={r:BundleRenderer(r,lesson['paired_edition'][r+'_pages'],{'review_footer':'Chapter six / Educational review edition'},[lesson],output_dir=OUT,files=FILES,label='Numbers to ninety-nine').build() for r in FILES}
assert sha(FILES['workbook'])==baseline['hashes'][str(FILES['workbook'].relative_to(ROOT)).replace('\\','/')]
for path,digest in before_rasters.items():
 if path.replace('\\','/')!='output/chapter-6/textbook/page-21.png':assert sha(ROOT/path)==digest,path
assert sha(archive/FILES['textbook'].name)==baseline['hashes'][str(FILES['textbook'].relative_to(ROOT)).replace('\\','/')]
(archive/'correction-validation.json').write_text(json.dumps(dict(authorized_delta='Only P1-06 TB21 credit: provenance manifest + matching sidecar',old_pdf_sha=sha(archive/FILES['textbook'].name),new_pdf_sha=sha(FILES['textbook']),workbook_bytes_unchanged=True,other_20_textbook_and_14_workbook_rasters_unchanged=True),indent=2)+'\n')
print('Prior chapter credit correction passed exact canonical/raster/workbook preservation.')
