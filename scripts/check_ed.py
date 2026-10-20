"""Recompute every reported small-system ED reference independently of TeNPy."""
import json
from pathlib import Path
from qground.evaluator import case_by_id
from qground.exactdiag import reference

def main():
    n=0
    for name in ['dev','heldout']:
        path=Path(f'results/pilot/{name}-ed.json')
        for cid,old in json.loads(path.read_text()).items():
            new=reference(case_by_id(cid))
            assert abs(old['energy']-new['energy'])<1e-10
            assert new['residual_norm']<1e-9
            n+=1
    p=Path('research/contributor-001/ed.json')
    if p.exists():
        cases={c['id']:c for c in json.loads(p.with_name('fresh-suite.json').read_text())['instances']}
        for cid,old in json.loads(p.read_text()).items():
            new=reference(cases[cid])
            assert abs(old['energy']-new['energy'])<1e-10
            assert new['residual_norm']<1e-9
            n+=1
    sp=Path('research/contributor-001/supplement/ed.json')
    if sp.exists():
        cases={c['id']:c for c in json.loads(sp.with_name('preregistration.json').read_text())['instances']}
        for cid,old in json.loads(sp.read_text()).items():
            new=reference(cases[cid]);assert abs(old['energy']-new['energy'])<1e-10
            assert new['residual_norm']<1e-9;n+=1
    print(f'PASS: {n} full-Hilbert-space numerical ED references; residuals <1e-9; energies agree <1e-10')
if __name__=='__main__':main()
