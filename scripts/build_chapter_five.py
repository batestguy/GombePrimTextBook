"""Build P1-05 canonical A bundle of ten textbook/workbook continuation."""
import hashlib
import json
from build_primary_one_opening import ROOT, EXPECTED_HASH, Renderer, read, GREEN, INK, H
from check_chapter_standard import validate

OUT=ROOT/'output/chapter-5'
FILES={role:ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Bundle-of-ten-{role.title()}.pdf'
       for role in ('textbook','workbook')}


class BundleRenderer(Renderer):
    """A bundle expands to ten separate countable vector strips, not one icon."""
    def object_at(self,kind,x,top,scale=1):
        if kind!='strip':return super().object_at(kind,x,top,scale)
        c=self.c; c.saveState(); c.translate(x,H-top); c.scale(scale,scale)
        c.setLineWidth(.8); c.setStrokeColor(INK); c.setFillColor(GREEN)
        c.rect(-2,-52,4,52,stroke=1,fill=1); c.restoreState()

    def element(self,el):
        if el['type']!='bundle':return super().element(el)
        x,y,s=el['x'],el['top'],el.get('scale',1)
        super().element(dict(type='objects',id=el['id'],kind='strip',count=10,
            points=[[x+i*6*s,y] for i in range(10)],scale=s))
        # Two open binding lines add no assessed objects or filled marks.
        for dy in (23,29):
            super().element(dict(type='line',x1=x-4*s,top1=y+dy*s,
                                x2=x+58*s,top2=y+dy*s))


def build():
    validate()
    assert hashlib.sha256((ROOT/'GombeTextbook.txt').read_bytes()).hexdigest()==EXPECTED_HASH
    lesson=next(x for x in read('production/p1.json') if x['id']=='P1-05')
    pair=lesson['paired_edition']
    assert pair['teacher_id']=='ms-binta' and pair['objective_ids']==['P1-p02-06','P1-p02-07']
    assert pair['source_tasks']==[dict(id=f'P1-05-Q{i}',source_prompt=q['prompt'],source_answer=q['answer'])
                                  for i,q in enumerate(lesson['questions'],1)]
    OUT.mkdir(parents=True,exist_ok=True); FILES['textbook'].parent.mkdir(parents=True,exist_ok=True)
    reports={}
    for role in FILES:
        pages=pair[role+'_pages']
        reports[role]=BundleRenderer(role,pages,{'review_footer':'Chapter five / Educational review edition'},
            [lesson],output_dir=OUT,files=FILES,label='A bundle of ten').build()
        assert all(q['id'] in reports[role]['task_pages'] for q in pair['source_tasks'])
        ledger={x['id']:x for x in reports[role]['objects']}
        for page in pages:
            for el in page['elements']:
                if el['type']=='bundle':assert ledger[el['id']]['count']==10
    objects={x['id']:x for x in reports['textbook']['objects']}
    for n in range(11,21):
        ids=[f'c5-ladder-{n}-ten-a',f'c5-ladder-{n}-ones'] if n<20 else ['c5-ladder-20-ten-a','c5-ladder-20-ten-b']
        assert sum(objects[k]['count'] for k in ids)==n
    assert objects['c5-ending-ten-a']['count']+objects['c5-ending-ten-b']['count']==20
    (OUT/'validation.json').write_text(json.dumps(dict(chapters=['P1-05'],
        artifacts={k:str(v.relative_to(ROOT)) for k,v in FILES.items()},pages={k:v['pages'] for k,v in reports.items()},
        source_hash=EXPECTED_HASH,status='draft_continuation_built_independent_review_required'),indent=2)+'\n',encoding='utf-8')
    print('Built A bundle of ten:',', '.join(f"{k}: {v['pages']} A4 pages" for k,v in reports.items()))


if __name__=='__main__':build()
