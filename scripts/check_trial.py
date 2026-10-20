"""Portable replay of contributor witnesses, independent of TeNPy."""
import json
from pathlib import Path
import time
from qground.evaluator import case_by_id,verify,digest
OUT=Path('research/contributor-001')

def main():
    start=time.perf_counter();count=0
    cases={c['id']:c for c in json.loads((OUT/'fresh-suite.json').read_text())['instances']}
    for part in ['dev','test']:
        for r in json.loads((OUT/f'{part}.json').read_text()):
            c=cases[r['instance']] if r['instance'] in cases else case_by_id(r['instance'])
            v=verify(r['witness'],c,r['energy'])
            assert v['energy_interval']==r['energy_interval']
            assert v['witness_sha256']==r['witness_sha256']
            count+=1
    selection=json.loads((OUT/'selection.json').read_text())
    for p,h in selection['source_hashes'].items():
        assert digest(p)==h, 'trial source changed: '+p
    print(f'PASS: {count} contributor witnesses and frozen source hashes; {time.perf_counter()-start:.2f}s')

if __name__=='__main__':main()
