"""Short contributor trial. Separate from the frozen initial experiment code."""
import argparse
import copy
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import secrets
import time
import numpy as np
from tenpy.networks.mps import MPS
from tenpy.algorithms.dmrg import TwoSiteDMRGEngine, SingleSiteDMRGEngine
from qground.optimize import model, arrays, save, run as baseline_run
from qground.evaluator import case_by_id, verify, digest
from qground.exactdiag import reference

OUT=Path('research/contributor-001')
METHODS=['nnn_dimers','continuation','hybrid_polish']

def write(path,obj):
    Path(path).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')

def now():return datetime.now(timezone.utc).isoformat()

def hashes():
    paths=[Path(__file__),*Path('qground').glob('*.py')]
    return {str(p.resolve().relative_to(Path.cwd())):digest(p) for p in paths}

def proposed(case,method,directory):
    c0,w0=time.process_time(),time.perf_counter()
    m=model(case); sites=m.lat.mps_sites();L=case['L']
    if method=='nnn_dimers':
        pairs=[]
        for i in range(0,L-3,4): pairs.extend([(i,i+2),(i+1,i+3)])
        if L%4==2:pairs.append((L-2,L-1))
        psi=MPS.from_singlets(sites[0],L,pairs)
    elif method=='continuation':
        psi=MPS.from_singlets(sites[0],L,[(i,i+1) for i in range(0,L,2)])
    elif method=='hybrid_polish':
        psi=MPS.from_product_state(sites,['up','down']*(L//2),bc='finite')
    else: raise ValueError(method)
    options={'trunc_params':{'chi_max':8,'svd_min':1e-14,'trunc_cut':None},
        'mixer':True,'mixer_params':{'amplitude':1e-5,'decay':10.,'disable_after':3},
        'diag_method':'lanczos','lanczos_params':{'N_max':40,'N_min':2,'P_tol':1e-12,'E_tol':1e-12},'combine':True}
    engine=TwoSiteDMRGEngine(psi,m,copy.deepcopy(options));engine.pre_run_initialize()
    history=[];ec=ew=0.;updates=iters=0
    for k in range(6):
        if method=='continuation':
            # Two easy dimer-near sweeps, then four target sweeps. All work is charged.
            target={**case,'J2':'0.5'} if k<2 else case
            if k in (0,2):
                if k:updates+=len(engine.update_stats['i0']);iters+=sum(engine.update_stats['N_lanczos'])
                engine=TwoSiteDMRGEngine(psi,model(target),copy.deepcopy(options))
                engine.pre_run_initialize()
        if method=='hybrid_polish' and k==3:
            updates+=len(engine.update_stats['i0']);iters+=sum(engine.update_stats['N_lanczos'])
            polish=copy.deepcopy(options);polish['mixer']=False;polish.pop('mixer_params')
            engine=SingleSiteDMRGEngine(psi,m,polish);engine.pre_run_initialize()
        engine.sweep();engine.mixer_cleanup()
        snap=psi.copy();snap.canonical_form()
        cpu=time.process_time()-c0-ec;wall=time.perf_counter()-w0-ew
        a,b=time.process_time(),time.perf_counter()
        path=directory/f'sweep-{k+1}.npz'
        save(path,arrays(snap),case)
        history.append({'sweep':k+1,'cpu_seconds':cpu,'wall_seconds':wall,
            'witness':str(path),'optimizer_energy':float(m.H_MPO.expectation_value(snap))})
        ec+=time.process_time()-a;ew+=time.perf_counter()-b
    updates+=len(engine.update_stats['i0']);iters+=sum(engine.update_stats['N_lanczos'])
    return {'instance':case['id'],'method':method,'seed':1729,'history':history,
        'cpu_seconds':history[-1]['cpu_seconds'],'wall_seconds':history[-1]['wall_seconds'],
        'local_updates':updates,'lanczos_iterations':int(iters),'options':options}

def execute(case,method,label,seed=1729):
    started_at=now()
    directory=OUT/'witnesses'/f'{case["id"]}-{label}-{seed}'
    directory.mkdir(parents=True,exist_ok=False)
    if method in METHODS:r=proposed(case,method,directory)
    else:r=baseline_run(case,method,seed,directory,6)
    start=time.perf_counter()
    for h in r['history']:h.update(verify(h['witness'],case,h['optimizer_energy']))
    best=min(r['history'],key=lambda h:h['energy'])
    r.update({k:best[k] for k in ('energy','energy_interval','witness','witness_sha256')})
    r['best_sweep']=best['sweep'];r['run_label']=label
    r['verification_seconds']=time.perf_counter()-start
    r['started_at']=started_at;r['finished_at']=now()
    write(directory/'run.json',r)
    print(f'{case["id"]} {label}: E={r["energy"]:.12f}, cpu={r["cpu_seconds"]:.3f}, verify={r["verification_seconds"]:.3f}',flush=True)
    return r

def main():
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['dev','test']);a=p.parse_args()
    if a.phase=='dev':
        if (OUT/'dev.json').exists():raise ValueError('development already run')
        write(OUT/'hypothesis.json',{'frozen_at':now(),'source_hashes':hashes(),
            'hypotheses':{'nnn_dimers':'When J2 dominates, use singlets along J2 bonds to seed the two interleaved chains.',
            'continuation':'Initialize near the dimerized J2=0.5 regime, then spend four of six sweeps on the frozen target.',
            'hybrid_polish':'Two-site updates grow the basis but truncate after minimization; use three two-site sweeps then three fixed-bond single-site sweeps without mixer.'},
            'selection':'best mean per-site development gain over baseline; threshold 1e-10; consider established dimer as fallback; no test data used'})
        dev=[]
        for cid in ['dev10','dev12','dev24']:
            for method in METHODS:dev.append(execute(case_by_id(cid),method,method))
        write(OUT/'dev.json',dev)
        existing=json.loads(Path('results/pilot/dev.json').read_text())
        baseline={r['instance']:r for r in existing if r['method']=='baseline' and r['seed']==1729}
        allrows=dev+[r for r in existing if r['seed']==1729 and r['method']!='baseline']
        scores={m:sum((r['energy']-baseline[r['instance']]['energy'])/case_by_id(r['instance'])['L']
            for r in allrows if r['method']==m)/3 for m in sorted({r['method'] for r in allrows})}
        selected=min(scores,key=scores.get)
        write(OUT/'selection.json',{'selected':selected,'scores_per_site':scores,'frozen_at':now(),'source_hashes':hashes()})
        # Draw public fresh instances only after fixing the selected method. No fit to these draws.
        seed=secrets.token_hex(16);rng=np.random.default_rng(int(seed,16))
        cases=[]
        for L in [16,20,32]:
            j2=int(rng.integers(5,21))/16
            delta=float(rng.choice([1.,1.25]))
            cases.append({'id':f'fresh{L}','L':L,'J1':'1','J2':str(j2),'delta':str(delta),
                'boundary':'open','basis':'down,up','chi_max':8,'split':'fresh-heldout'})
        write(OUT/'fresh-suite.json',{'seed':seed,'drawn_at':now(),'instances':cases,
            'generator':'NumPy default_rng(int(seed,16)); L=16,20,32; J2=integers(5,21)/16; delta=choice([1,1.25])',
            'note':'Local OS randomness after method freeze, not a public beacon or secret sealed set.'})
        print('TRIAL SELECTED',selected,flush=True)
    else:
        selection=json.loads((OUT/'selection.json').read_text())
        assert selection['source_hashes']==hashes(),'method changed after selection'
        if (OUT/'test.json').exists():raise ValueError('already tested')
        cases=json.loads((OUT/'fresh-suite.json').read_text())['instances'];rows=[]
        strong_method=json.loads(Path('results/pilot/selection.json').read_text())['selected']
        for i,c in enumerate(cases):
            order=[('baseline','baseline'),(selection['selected'],'selected'),(strong_method,'strong-control'),('baseline','aa')]
            order=order[i:]+order[:i]
            for m,label in order:rows.append(execute(c,m,label))
        write(OUT/'test.json',rows)
        write(OUT/'ed.json',{c['id']:reference(c) for c in cases if c['L']<=16})

if __name__=='__main__':main()
