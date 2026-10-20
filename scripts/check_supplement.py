import json
from pathlib import Path
from qground.evaluator import verify,digest

def main():
    root=Path('research/contributor-001/supplement')
    reg=json.loads((root/'preregistration.json').read_text())
    assert digest('scripts/supplement.py')==reg['supplement_script_sha256']
    cases={c['id']:c for c in reg['instances']};n=0
    for r in json.loads((root/'runs.json').read_text()):
        v=verify(r['witness'],cases[r['instance']],r['energy'])
        assert v['energy_interval']==r['energy_interval']
        assert v['witness_sha256']==r['witness_sha256'];n+=1
    long=Path('research/contributor-001/long-reference/run.json')
    if long.exists():
        from qground.evaluator import case_by_id
        r=json.loads(long.read_text());h=r['best']
        v=verify(h['witness'],case_by_id(r['instance']),h['energy'])
        assert v['energy_interval']==h['energy_interval'];n+=1
    print(f'PASS: {n} supplemental/reference witnesses and supplement code hash')
if __name__=='__main__':main()
