"""A stronger convergence reference; explicitly NOT an equal-budget competitor."""
import json
from pathlib import Path
from qground.optimize import run
from qground.evaluator import verify,case_by_id

def main():
    out=Path('research/contributor-001/long-reference')
    out.mkdir(parents=True,exist_ok=False)
    c=case_by_id('dev24')
    r=run(c,'baseline',1729,out,24)
    checked=[]
    for h in r['history']:
        if h['sweep'] in [6,12,18,24]:
            h.update(verify(h['witness'],c,h['optimizer_energy']));checked.append(h)
    r['checkpoints']=checked
    r['purpose']='24-sweep fixed-chi reference; 4x sweep budget; not a matched-budget win'
    (out/'run.json').write_text(json.dumps(r,indent=2)+'\n')
    print([(h['sweep'],h['energy']) for h in checked])
if __name__=='__main__':main()
