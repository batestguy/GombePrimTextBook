"""Build P1-04 Six to nine as a canonical textbook/workbook continuation."""
import hashlib
import json

from build_primary_one_opening import ROOT, EXPECTED_HASH, Renderer, read, BLUE, INK
from check_chapter_standard import validate

OUT=ROOT/'output/chapter-4'
FILES={role:ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Six-to-nine-{role.title()}.pdf'
       for role in ('textbook','workbook')}


class ShapeRenderer(Renderer):
    """Exact paper shapes; shared renderer and earlier PDFs remain untouched."""
    def object_at(self,kind,x,top,scale=1):
        if kind not in ('disc','square','triangle','rectangle'):
            return super().object_at(kind,x,top,scale)
        from build_primary_one_opening import H
        c=self.c
        c.saveState(); c.translate(x,H-top); c.scale(scale,scale)
        c.setLineWidth(1.1); c.setStrokeColor(INK); c.setFillColor(BLUE)
        if kind=='disc':c.circle(0,0,14,stroke=1,fill=1)
        elif kind=='square':c.rect(-14,-14,28,28,stroke=1,fill=1)
        elif kind=='rectangle':c.rect(-17,-10,34,20,stroke=1,fill=1)
        else:
            path=c.beginPath(); path.moveTo(0,16); path.lineTo(-16,-13)
            path.lineTo(16,-13); path.close(); c.drawPath(path,stroke=1,fill=1)
        c.restoreState()


def build():
    validate()
    assert hashlib.sha256((ROOT/'GombeTextbook.txt').read_bytes()).hexdigest()==EXPECTED_HASH
    l=next(x for x in read('production/p1.json') if x['id']=='P1-04')
    pair=l['paired_edition']
    assert pair['teacher_id']=='mr-aliyu'
    assert pair['objective_ids']==[f'P1-p02-0{i}' for i in range(1,6)]
    assert pair['source_tasks']==[dict(id=f'P1-04-Q{i}',source_prompt=q['prompt'],source_answer=q['answer'])
                                  for i,q in enumerate(l['questions'],1)]
    OUT.mkdir(parents=True,exist_ok=True)
    FILES['textbook'].parent.mkdir(parents=True,exist_ok=True)
    reports={}
    for role in FILES:
        reports[role]=ShapeRenderer(role,pair[role+'_pages'],
            {'review_footer':'Chapter four / Educational review edition'},[l],
            output_dir=OUT,files=FILES,label='Six to nine').build()
        assert all(q['id'] in reports[role]['task_pages'] for q in pair['source_tasks'])
        assert all(s in reports[role]['task_pages'] for s in ('P1-04-S002','P1-04-S003','P1-04-S004'))
    objects={x['id']:x for x in reports['textbook']['objects']}
    for word,n in [('six',6),('seven',7),('eight',8),('nine',9)]:
        assert objects['c4-model-'+word]['count']==n
        assert objects['c4-ending-'+word]['count']==n
    assert sum(objects['c4-ending-'+x]['count'] for x in ('six','seven','eight','nine'))==30
    (OUT/'validation.json').write_text(json.dumps(dict(chapters=['P1-04'],
        artifacts={k:str(v.relative_to(ROOT)) for k,v in FILES.items()},
        pages={k:v['pages'] for k,v in reports.items()},source_hash=EXPECTED_HASH,
        status='draft_continuation_built_independent_review_required'),indent=2)+'\n',encoding='utf-8')
    print('Built Six to nine:',', '.join(f"{k}: {v['pages']} A4 pages" for k,v in reports.items()))


if __name__=='__main__':build()
