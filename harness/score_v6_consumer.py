"""Frozen v6 scorer: unknown histories are not negative labels."""
import json, itertools, csv
from pathlib import Path
R=Path(__file__).resolve().parents[1]
DOMAINS=['career','relationship','study','finance']
NEAR=[{'job_start','job_change'},{'business_failure','job_loss'},{'relationship_start','marriage'},{'breakup','divorce'}]
OPPOSITES=[{'up','down'},{'advance','setback'},{'forming','ending'},{'conflict','stable'},{'ending','stable'},{'down','stable'},{'setback','stable'}]
JARGON=['喜用神','忌神','十神','七杀','正官','偏官','化忌','四化','命宫','夫妻宫','大运','流年','Dasha','Mahadasha','伤官','比劫','印星']
def match(a,b):
 if a.get('domain')!=b.get('domain'):return 0.
 x,y=a.get('event_code'),b.get('event_code')
 return 1. if x==y else .5 if any(x in g and y in g for g in NEAR) else 0.
def timeweight(a,b):
 y=a.get('year')
 if not isinstance(y,int):return 0.
 lo=b.get('year',b.get('start_year'));hi=b.get('year',b.get('end_year'))
 d=max(lo-y,y-hi,0)
 return {0:1.,1:.7,2:.4}.get(d,0.)
def reverse(a,b):return any(a in x and b in x and a!=b for x in OPPOSITES)
def score_one(a,g):
 raw=a.get('events',[]) if isinstance(a.get('events',[]),list) else []
 ps=[];counts={d:0 for d in DOMAINS}
 for p in raw[:4]:
  if not isinstance(p,dict) or p.get('domain') not in DOMAINS:continue
  d=p['domain'];counts[d]+=1
  if counts[d]<=2:ps.append(p)
 gs=g['targets'];n=len(gs);pairs=[];best=(-1,-1)
 # Each target and prediction used at most once. Prefer more exact events, then timing.
 def search(i,used,picked):
  nonlocal best,pairs
  if i==len(ps):
   value=(sum(match(ps[x],gs[y]) for x,y in picked),sum(match(ps[x],gs[y])*timeweight(ps[x],gs[y]) for x,y in picked))
   if value>best:best=value;pairs=picked[:]
   return
  search(i+1,used,picked)
  for j,z in enumerate(gs):
   if j not in used and match(ps[i],z):search(i+1,used|{j},picked+[(i,j)])
 search(0,set(),[])
 event=best[0]/n if n else 0;timing=best[1]/n if n else 0
 directions=a.get('domains',{});correct=bad=0;checks=[]
 for d,v in g['directions'].items():
  p=directions.get(d,'uncertain');p=p.get('direction','uncertain') if isinstance(p,dict) else p
  correct+=p==v;bad+=reverse(p,v);checks.append({'domain':d,'predicted':p,'actual':v,'correct':p==v,'reverse':reverse(p,v)})
 dn=len(checks);direction=correct/dn if dn else 0;penalty=10*bad/dn if dn else 0
 used={i for i,j in pairs};verifiable=len(used);unknown=0;wrong=0
 # Only opposite explicit directions establish an incorrect unpaired event.
 for i,p in enumerate(ps):
  if i in used:continue
  d=p['domain'];pd=event_direction(p['event_code'],d)
  if d in g['directions'] and reverse(pd,g['directions'][d]):wrong+=1;verifiable+=1
  else:unknown+=1
 precision=best[0]/verifiable if verifiable else 0
 summary=a.get('plain_summary','');advice=a.get('practical_advice','');follow=a.get('followup_questions',[])
 answered=bool(ps or any((directions.get(d) or 'uncertain')!='uncertain' for d in DOMAINS)) and not a.get('abstain_reason')
 ease=0
 if answered:
  ease+=all(d in directions for d in DOMAINS)
  ease+=bool(summary) and len(summary)<=120 and not any(t in summary for t in JARGON)
  ease+=bool(ps) and all(bool(p.get('event_text')) and len(p['event_text'])<=100 for p in ps)
  ease+=bool(advice) and len(advice)<=80 and any(x in advice for x in ['核','查','记','列','沟通','准备','比较','预算','确认','保存','复习','咨询','计划','学习','避免','先','问','联系','不要','检查','收集'])
  ease+=not follow or bool(a.get('missing_info'))
 return {'case_id':g['case_id'],'event_score':45*event,'direction_score':25*direction,'time_score':15*timing,'specific_score':5*precision,'ease_score':ease,'reverse_penalty':penalty,'accuracy85':45*event+25*direction+15*timing-penalty,'base95':45*event+25*direction+15*timing+5*precision+ease-penalty,'targets':n,'matched_exact':sum(match(ps[i],gs[j])==1 for i,j in pairs),'matched_near':sum(match(ps[i],gs[j])==.5 for i,j in pairs),'matched_weight':best[0],'direction_checks':checks,'directions_correct':correct,'directions_reverse':bad,'directions_tested':dn,'unknown_claims':unknown,'wrong_claims':wrong,'predicted_events':len(ps),'answered':answered,'format_violation':len(raw)>4 or any(v>2 for v in counts.values()),'pairs':[{'prediction':ps[i],'target':gs[j],'event_weight':match(ps[i],gs[j]),'time_weight':timeweight(ps[i],gs[j])} for i,j in pairs]}
def event_direction(code,domain):
 maps={'career':{'job_start':'up','promotion':'up','business_start':'up','job_loss':'down','business_failure':'down','job_change_failed':'down','business_plan_failed':'down','job_change':'change','job_leave_voluntary':'change'},'relationship':{'marriage':'forming','relationship_start':'forming','breakup':'ending','divorce':'ending','relationship_conflict':'conflict'},'study':{'study_entry':'advance','graduation':'advance','study_delay':'setback','study_dropout':'setback'},'finance':{'financial_gain':'up','financial_loss':'down'}}
 return maps.get(domain,{}).get(code,'uncertain')
def load_rows(path):
 x=json.loads(path.read_text());return x if isinstance(x,list) else x.get('answers',x.get('results',[]))
def run():
 gold=[json.loads(x) for x in (R/'datasets/gold/v6-events.jsonl').read_text().splitlines()];index={x['case_id']:x for x in gold};summaries=[];allrows=[]
 for file in sorted((R/'runs/v6-consumer-events/answers').glob('*.json')):
  rows=load_rows(file);ai={x['case_id']:x for x in rows};scores=[score_one(ai.get(g['case_id'],{'case_id':g['case_id'],'abstain_reason':'未交付'}),g) for g in gold]
  cp=R/'runs/v6-consumer-events/controls'/file.name;control=load_rows(cp) if cp.exists() else [];ci={x['case_id']:x for x in control};control_ids=['V01','V02','V03','V04','V05'];valid=all(x in ci for x in control_ids)
  lift=0;delta=None
  if valid:
   yes=sum(next(x for x in scores if x['case_id']==c)['accuracy85'] for c in control_ids)/5
   no=sum(score_one(ci[c],index[c])['accuracy85'] for c in control_ids)/5;delta=yes-no;lift=min(5,max(0,delta/85*5))
  avg=lambda k:sum(x[k] for x in scores)/len(scores)
  total=max(0,avg('base95')+lift)
  entry={'config':file.stem,'case_count':len(gold),'score':round(total,2),'accuracy85':round(avg('accuracy85'),2),'event45':round(avg('event_score'),2),'direction25':round(avg('direction_score'),2),'time15':round(avg('time_score'),2),'specific5':round(avg('specific_score'),2),'wrong_input5':round(lift,2),'ease5':round(avg('ease_score'),2),'reverse_penalty':round(avg('reverse_penalty'),2),'wrong_input_complete':valid,'wrong_input_delta85':delta,'answered':sum(x['answered'] for x in scores),'targets':sum(x['targets'] for x in scores),'exact_events':sum(x['matched_exact'] for x in scores),'near_events':sum(x['matched_near'] for x in scores),'directions_correct':sum(x['directions_correct'] for x in scores),'directions_tested':sum(x['directions_tested'] for x in scores),'directions_reverse':sum(x['directions_reverse'] for x in scores),'unknown_claims':sum(x['unknown_claims'] for x in scores),'wrong_claims':sum(x['wrong_claims'] for x in scores),'format_violations':sum(x['format_violation'] for x in scores),'per_domain':{}}
  for d in DOMAINS:
   ids=[g['case_id'] for g in gold if d in g['directions']];subset=[x for x in scores if x['case_id'] in ids];entry['per_domain'][d]={'supported_people':len(ids),'direction_correct':sum(c['correct'] for x in subset for c in x['direction_checks'] if c['domain']==d),'direction_reverse':sum(c['reverse'] for x in subset for c in x['direction_checks'] if c['domain']==d),'event_targets':sum(z['domain']==d for g in gold for z in g['targets']),'event_exact':sum(z['target']['domain']==d and z['event_weight']==1 for x in scores for z in x['pairs'])}
  summaries.append(entry);allrows.extend({'config':file.stem,**x} for x in scores)
 out=R/'reports';(out/'v6-consumer-scores.json').write_text(json.dumps({'ranking':sorted(summaries,key=lambda x:-x['score']),'details':allrows},ensure_ascii=False,indent=2))
 with (out/'v6-consumer-results.csv').open('w') as f:
  keys=['config','case_id','targets','matched_exact','matched_near','directions_tested','directions_correct','directions_reverse','unknown_claims','wrong_claims','answered','accuracy85','base95'];w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(allrows)
 print(json.dumps(summaries,ensure_ascii=False))
if __name__=='__main__':run()
