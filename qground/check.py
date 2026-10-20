"""Fresh-process witness verification and recorded-result replay."""
import argparse
import json
import time
from pathlib import Path
from .evaluator import verify, case_by_id, digest


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--witness');p.add_argument('--case');p.add_argument('--claim')
    p.add_argument('--results',default='results/pilot')
    p.add_argument('--all-checkpoints',action='store_true')
    args=p.parse_args()
    if args.witness:
        print(json.dumps(verify(args.witness,case_by_id(args.case),args.claim),indent=2));return
    start=time.perf_counter();count=0
    for filename in ['dev.json','heldout.json']:
        rows=json.loads((Path(args.results)/filename).read_text())
        for r in rows:
            items=r['history'] if args.all_checkpoints else [r]
            for item in items:
                report=verify(item['witness'],case_by_id(r['instance']),item['energy'])
                assert report['witness_sha256']==item['witness_sha256'], 'witness hash mismatch'
                assert report['energy_interval']==item['energy_interval'], 'interval mismatch'
                count+=1
    print(f'PASS: {count} witnesses; exact rational energies and normalization; {time.perf_counter()-start:.2f}s')

if __name__=='__main__':main()
