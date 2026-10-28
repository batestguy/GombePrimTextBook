"""Build the canonical P1-03 continuation textbook/workbook; preserve opening PDFs.

Run python scripts/build_chapter_three.py. This is not the full annual assembly.
Independent every-task/page review of both artifacts is required after changes.
"""
import hashlib
import json

from build_primary_one_opening import ROOT, EXPECTED_HASH, Renderer, read
from check_chapter_standard import validate

OUT = ROOT/'output/chapter-3'
FILES = {role: ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Zero-{role.title()}.pdf'
         for role in ('textbook','workbook')}


def build():
    validate()
    assert hashlib.sha256((ROOT/'GombeTextbook.txt').read_bytes()).hexdigest() == EXPECTED_HASH
    lesson = next(x for x in read('production/p1.json') if x['id']=='P1-03')
    pair = lesson['paired_edition']
    assert pair['teacher_id']=='ms-binta'
    assert pair['objective_ids']==['P1-p01-06','P1-p01-07','P1-p01-08']
    assert pair['source_tasks']==[
        dict(id=f'P1-03-Q{i}',source_prompt=q['prompt'],source_answer=q['answer'])
        for i,q in enumerate(lesson['questions'],1)]
    OUT.mkdir(parents=True,exist_ok=True)
    FILES['textbook'].parent.mkdir(parents=True,exist_ok=True)
    reports={}
    for role in FILES:
        reports[role]=Renderer(role,pair[role+'_pages'],
                               {'review_footer':'Chapter three / Educational review edition'},[lesson],
                               output_dir=OUT,files=FILES,label='Zero').build()
        assert all(t['id'] in reports[role]['task_pages'] for t in pair['source_tasks'])
        # None must remain an exact empty set; not merely an unverified caption.
        empty=[d for d in reports[role]['objects'] if 'empty' in d['id'] or 'none' in d['id']]
        assert empty and all(d['count']==0 and not d['kinds'] for d in empty)
    manifest=dict(chapters=['P1-03'],artifacts={k:str(v.relative_to(ROOT)) for k,v in FILES.items()},
                  pages={k:v['pages'] for k,v in reports.items()},source_hash=EXPECTED_HASH,
                  status='draft_continuation_pair_built_independent_review_required')
    (OUT/'validation.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('Built zero continuation:',', '.join(f"{k}: {v['pages']} A4 pages" for k,v in reports.items()))


if __name__=='__main__':
    build()
