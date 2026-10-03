"""Apply blinded text eligibility review, preserving the frozen scoring weights."""
import json,hashlib
from pathlib import Path
import score_v6_consumer as S
R=S.R
ORIGINAL_LOAD=S.load_rows;ORIGINAL_SCORE=S.score_one
annotations=json.loads((R/'runs/v6-consumer-events/adjudications.json').read_text())
index={}
for a in annotations:
 if not isinstance(a['case_id'],str) or not a['case_id'].startswith('V'):raise ValueError('Audit case_id must be actual Vxx: '+str(a))
 key=(a['group'],a['config'],a['case_id']);index.setdefault(key,{})[a['event_index']]=a

def load_rows(p):
 rows=ORIGINAL_LOAD(p);group=p.parent.name
 for row in rows:
  marks=index.get((group,p.stem,row['case_id']),{});events=row.get('events',[]);kept=[];dropped=[]
  for i,e in enumerate(events):
   if i in marks:
    a=marks[i]
    if e.get('event_text')!=a['original_event_text']:raise ValueError('Stale/mismatched text annotation: '+str(a))
    dropped.append({'event':e,'quality':a['quality'],'reason':a['reason']})
   else:kept.append(e)
  row['events']=kept;row['_excluded_events']=dropped
 return rows

def score_one(a,g):
 z=ORIGINAL_SCORE(a,g);z['generic_or_miscoded']=len(a.get('_excluded_events',[]));z['excluded_events']=a.get('_excluded_events',[]);return z
S.load_rows=load_rows;S.score_one=score_one
S.run()
p=R/'reports/v6-consumer-scores.json';z=json.loads(p.read_text())
for row in z['ranking']:row['generic_or_miscoded']=sum(x['generic_or_miscoded'] for x in z['details'] if x['config']==row['config'])
z['semantic_review']={'annotations_sha256':hashlib.sha256((R/'runs/v6-consumer-events/adjudications.json').read_bytes()).hexdigest(),'policy':'enforces predeclared generic statements do not count; no weight/target/date changes','reviewer':'separate gpt-6-luna agent without outcome/score access; not independent human review'}
p.write_text(json.dumps(z,ensure_ascii=False,indent=2))
