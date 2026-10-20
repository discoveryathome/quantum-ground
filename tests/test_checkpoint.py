"""Regression for the intermediate single-site export caught by exact checking."""
from qground.optimize import run
from qground.evaluator import verify

def test_single_site_all_checkpoints(tmp_path):
    c=dict(id='check',L=6,J1='1',J2='0.625',delta='1.25',boundary='open',basis='down,up',chi_max=8)
    r=run(c,'single_site',1729,tmp_path,6)
    for h in r['history']:
        report=verify(h['witness'],c,h['optimizer_energy'])
        assert report['max_bond']<=8
