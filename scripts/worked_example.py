"""Known exact dimer solution; a positive control, never a research advance."""
from pathlib import Path
import json
import numpy as np
from qground.evaluator import case_by_id,hamiltonian_id,verify

def main():
    c=case_by_id('dev12');out=Path('examples');out.mkdir(exist_ok=True)
    a=np.zeros((1,2,2));a[0,0,0]=2**-0.5;a[0,1,1]=2**-0.5
    b=np.zeros((2,2,1));b[0,1,0]=1;b[1,0,0]=-1
    tensors=[a if i%2==0 else b for i in range(c['L'])]
    path=out/'known-dimer.npz'
    np.savez_compressed(path,hamiltonian_id=hamiltonian_id(c),**{f'A{i}':v for i,v in enumerate(tensors)})
    result=verify(path,c,-4.5)
    assert result['energy_interval']==['-4.50000000000000','-4.50000000000000']
    result.update({'instance':'dev12','witness':str(path),'method':'known-exact-dimer','by':'Known Majumdar–Ghosh construction',
        'source':'docs/FORMULATION.md#solved-positive-control-at-the-majumdarghosh-point','proven_lower_bound':'-9/2'})
    (out/'known-dimer.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
