import json
from pathlib import Path
lessons=[]
def L(c,slug,title,topic,pages,goal,look,learn,worked,play,words,hint,qs,diagram=''):
    items=[]
    for pair in qs.split('||'):
        question,answer=pair.split('=>')
        items.append({'prompt':question.strip(),'answer':answer.strip()})
    assert len(items)==6,(slug,len(items))
    lessons.append(dict(id=f'P{c}-{slug}',grade=c,title=title,topic=topic,source_pages=pages,goal=goal,look=look,learn=learn,worked=worked,play=play,vocabulary=words,hint=hint,questions=items,diagram=diagram))
def save(grade):
    Path(f'production/p{grade}.json').write_text(json.dumps(lessons,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Primary {grade}: {len(lessons)} lessons, {len(lessons)*6} questions')
