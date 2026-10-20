"""Predeclared development selection and one-shot held-out evaluation."""
import argparse
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
import platform
import subprocess
import time
import numpy as np
from threadpoolctl import threadpool_info
from .evaluator import suite, case_by_id, verify, digest, ROOT
from .exactdiag import reference
from .optimize import METHODS, run


def write(path, obj):
    Path(path).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')


def now():
    return datetime.now(timezone.utc).isoformat()


def source_hashes():
    return {str(p.relative_to(ROOT)):digest(p) for p in sorted((ROOT/'qground').glob('*.py'))}


def execute(c, method, seed, label, out):
    directory=out/'witnesses'/f'{c["id"]}-{label}-{seed}'
    directory.mkdir(parents=True,exist_ok=False)
    r=run(c,method,seed,directory,suite()['sweeps'])
    r['run_label']=label
    start=time.perf_counter()
    for item in r['history']:
        result=verify(item['witness'],c,item['optimizer_energy'])
        item.update(result)
    best=min(r['history'],key=lambda h: h['energy'])
    r.update({k:best[k] for k in ('energy','energy_interval','witness','witness_sha256')})
    r['best_sweep']=best['sweep']
    r['verification_seconds']=time.perf_counter()-start
    write(directory/'run.json',r)
    print(f'{c["id"]} {label} seed={seed}: E={r["energy"]:.12f}; CPU={r["cpu_seconds"]:.3f}s; verify={r["verification_seconds"]:.3f}s',flush=True)
    return r


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['dev','heldout'])
    parser.add_argument('--out',default='results/pilot')
    args=parser.parse_args()
    out=Path(args.out)
    out.mkdir(parents=True,exist_ok=True)
    config=suite()
    logging.basicConfig(level=logging.ERROR)
    lock_path=out/'preregistration.json'
    if args.phase=='dev':
        if lock_path.exists(): raise ValueError('output exists; use a new --out directory')
        write(lock_path,{'created_at':now(),'suite_sha256':digest(ROOT/'benchmarks/suite.json'),
            'source_hashes':source_hashes(),'methods':METHODS,'machine':platform.platform(),
            'python':platform.python_version(),'threads':threadpool_info(),
            'git_base':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
            'budget_note':'6 sweeps; each update Lanczos N_max=40; BLAS one thread; also common CPU checkpoints'})
        rows=[]
        for c in [c for c in config['instances'] if c['split']=='dev']:
            for rep,seed in enumerate(config['seeds']):
                # Counterbalance fixed method ordering; no concurrent benchmark jobs.
                methods=METHODS[rep:]+METHODS[:rep]
                for m in methods: rows.append(execute(c,m,seed,m,out))
        write(out/'dev.json',rows)
        base={(r['instance'],r['seed']):r for r in rows if r['method']=='baseline'}
        scores={m:float(np.mean([(r['energy']-base[(r['instance'],r['seed'])]['energy'])/case_by_id(r['instance'])['L']
                       for r in rows if r['method']==m])) for m in METHODS if m!='baseline'}
        top=min(scores.values())
        tied=[m for m,v in scores.items() if v <= top+1e-10]
        selected=min(tied,key=lambda m:np.mean([r['cpu_seconds'] for r in rows if r['method']==m]))
        write(out/'selection.json',{'selected':selected,'dev_scores_per_site':scores,
            'frozen_at':now(),'source_hashes':source_hashes(),'suite_sha256':digest(ROOT/'benchmarks/suite.json'),
            'policy':'best development alternative; selection does not assert improvement'})
        print('FROZEN SELECTION',selected,flush=True)
    else:
        selection=json.loads((out/'selection.json').read_text())
        assert selection['source_hashes']==source_hashes(), 'code changed after selection'
        assert selection['suite_sha256']==digest(ROOT/'benchmarks/suite.json'), 'suite changed'
        if (out/'heldout.json').exists(): raise ValueError('heldout already evaluated')
        rows=[]
        for c in [c for c in config['instances'] if c['split']=='heldout']:
            for rep,seed in enumerate(config['seeds']):
                methods=[('baseline','baseline'),(selection['selected'],'selected'),('baseline','aa')]
                methods=methods[rep:]+methods[:rep]
                for m,label in methods: rows.append(execute(c,m,seed,label,out))
        write(out/'heldout.json',rows)
    # ED references run outside the optimizer timing, and never feed its initial states.
    refs={c['id']:reference(c) for c in config['instances']
          if c['L']<=16 and c['split']==('dev' if args.phase=='dev' else 'heldout')}
    write(out/f'{args.phase}-ed.json',refs)

if __name__=='__main__': main()
