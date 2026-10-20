"""Transparent post-hoc coverage supplement; no method retuning or discarded draws."""
import json
from pathlib import Path
import secrets
import numpy as np
from scripts.contributor_trial import OUT,execute,write,now,hashes
from scripts.analyze import comparison,best
from qground.evaluator import verify,digest
from qground.exactdiag import reference


def main():
    selection=json.loads((OUT/'selection.json').read_text())
    assert selection['source_hashes']==hashes(),'selected method changed'
    root=OUT/'supplement';root.mkdir(exist_ok=False)
    seed=secrets.token_hex(16);rng=np.random.default_rng(int(seed,16))
    cases=[]
    # One new Hamiltonian in each non-dimer coupling regime, fixed before any scores.
    for L,low,high,delta in [(16,5,8,'1.25'),(20,9,13,'1'),(32,13,21,'1.25')]:
        cases.append({'id':f'coverage{L}','L':L,'J1':'1','J2':str(int(rng.integers(low,high))/16),
            'delta':delta,'boundary':'open','basis':'down,up','chi_max':8,'split':'post-hoc-coverage'})
    write(root/'preregistration.json',{'created_at':now(),'seed':seed,'instances':cases,
        'selected':selection['selected'],'selected_source_hashes':selection['source_hashes'],
        'supplement_script_sha256':digest(__file__),
        'reason':'Original fresh draw independently reproduced, but all three cases landed at the exactly dimerized J2=0.5 line. Preserve them and add stratified coverage, without method changes.',
        'generator':'default_rng(int(seed,16)); integers(5,8)/16 at L16; integers(9,13)/16 at L20; integers(13,21)/16 at L32; delta=1.25,1,1.25',
        'status':'Post-hoc additional test, not the preregistered primary test; no hypothesis retuning.',
        'budget':'six sweeps, chi<=8, same tolerances; compare common per-pair CPU ceilings; all trials reported'})
    strong=json.loads(Path('results/pilot/selection.json').read_text())['selected']
    rows=[]
    for i,c in enumerate(cases):
        order=[('baseline','coverage-baseline'),(selection['selected'],'coverage-selected'),(strong,'coverage-strong')]
        order=order[i:]+order[:i]
        for m,label in order:rows.append(execute(c,m,label))
    write(root/'runs.json',rows)
    pairs=[]
    for c in cases:
        b=next(r for r in rows if r['instance']==c['id'] and r['run_label']=='coverage-baseline')
        s=next(r for r in rows if r['instance']==c['id'] and r['run_label']=='coverage-selected')
        strongrow=next(r for r in rows if r['instance']==c['id'] and r['run_label']=='coverage-strong')
        budget=min(b['cpu_seconds'],s['cpu_seconds'])
        hb=[h for h in b['history'] if h['cpu_seconds']<=budget];hs=[h for h in s['history'] if h['cpu_seconds']<=budget]
        pairs.append({'instance':c['id'],'case':c,'baseline_energy':b['energy'],'candidate_energy':s['energy'],
            'strong_control_energy':strongrow['energy'],'strong_control_method':strong,
            'equal_sweeps':comparison(b,s),'matched_cpu':comparison(best(hb),best(hs)),
            'common_cpu_seconds':budget,'versus_initial_winner_equal_sweeps':comparison(strongrow,s),
            'candidate_cpu_ratio':s['cpu_seconds']/b['cpu_seconds']})
    write(root/'summary.json',{'selected':selection['selected'],'pairs':pairs,
        'counts':{metric:{k:sum(p[metric]['outcome']==k for p in pairs) for k in ['win','tie','loss']}
            for metric in ['equal_sweeps','matched_cpu','versus_initial_winner_equal_sweeps']},
        'optimizer_cpu_seconds':sum(r['cpu_seconds'] for r in rows),
        'optimizer_wall_seconds':sum(r['wall_seconds'] for r in rows),
        'verification_wall_seconds':sum(r['verification_seconds'] for r in rows),
        'status':'post-hoc stratified coverage; separate from primary test'})
    write(root/'ed.json',{c['id']:reference(c) for c in cases if c['L']<=16})
    print('Coverage supplement complete',flush=True)

if __name__=='__main__':main()
