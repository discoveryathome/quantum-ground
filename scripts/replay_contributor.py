"""Replay the archived search on its exact stored inputs, without redrawing tests."""
import argparse
import json
from pathlib import Path
import scripts.contributor_trial as trial
from qground.evaluator import case_by_id

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True)
    p.add_argument('--case');p.add_argument('--method');a=p.parse_args()
    original=Path('research/contributor-001')
    rows=json.loads((original/'dev.json').read_text())+json.loads((original/'test.json').read_text())
    rows+=json.loads((original/'supplement/runs.json').read_text())
    cases={c['id']:c for c in json.loads((original/'fresh-suite.json').read_text())['instances']}
    cases.update({c['id']:c for c in json.loads((original/'supplement/preregistration.json').read_text())['instances']})
    selected=[r for r in rows if (not a.case or r['instance']==a.case) and (not a.method or r['method']==a.method)]
    if not selected:raise ValueError('no matching archived run')
    trial.OUT=Path(a.out);trial.OUT.mkdir(parents=True,exist_ok=False)
    replay=[]
    for old in selected:
        c=cases[old['instance']] if old['instance'] in cases else case_by_id(old['instance'])
        new=trial.execute(c,old['method'],old['run_label'],old['seed'])
        new['archived_energy']=old['energy'];new['energy_drift']=new['energy']-old['energy']
        if abs(new['energy_drift'])>1e-9:raise AssertionError('replay energy drift exceeds 1e-9 J1')
        replay.append(new)
    (trial.OUT/'replay.json').write_text(json.dumps(replay,indent=2)+'\n')
    print(f'PASS: {len(replay)} optimizer replays, exact witness checks, energy drift <=1e-9 J1')
if __name__=='__main__':main()
