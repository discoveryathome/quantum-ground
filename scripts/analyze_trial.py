import json
from pathlib import Path
import statistics
from scripts.analyze import comparison,best
OUT=Path('research/contributor-001')

def main():
    data=json.loads((OUT/'test.json').read_text())
    cases={c['id']:c for c in json.loads((OUT/'fresh-suite.json').read_text())['instances']}
    pairs=[]
    for b in [r for r in data if r['run_label']=='baseline']:
        c=next(r for r in data if r['instance']==b['instance'] and r['run_label']=='selected')
        strong=next(r for r in data if r['instance']==b['instance'] and r['run_label']=='strong-control')
        aa=next(r for r in data if r['instance']==b['instance'] and r['run_label']=='aa')
        budget=min(b['cpu_seconds'],c['cpu_seconds'])
        hb=[h for h in b['history'] if h['cpu_seconds']<=budget]
        hc=[h for h in c['history'] if h['cpu_seconds']<=budget]
        matches=comparison(best(hb),best(hc)) if hb and hc else {'outcome':'insufficient checkpoints'}
        pairs.append({'instance':b['instance'],'case':cases[b['instance']],
            'equal_sweeps':comparison(b,c),'matched_cpu':matches,'common_cpu_seconds':budget,
            'versus_initial_winner_equal_sweeps':comparison(strong,c),'baseline_energy':b['energy'],
            'candidate_energy':c['energy'],'strong_control_energy':strong['energy'],'strong_control_method':strong['method'],
            'candidate_cpu_ratio':c['cpu_seconds']/b['cpu_seconds'],
            'aa_energy_difference':aa['energy']-b['energy'],'aa_cpu_ratio':aa['cpu_seconds']/b['cpu_seconds']})
    dev=json.loads((OUT/'dev.json').read_text())
    summary={'selected':json.loads((OUT/'selection.json').read_text())['selected'],'pairs':pairs,
        'equal_sweep_counts':{k:sum(x['equal_sweeps']['outcome']==k for x in pairs) for k in ['win','tie','loss']},
        'matched_cpu_counts':{k:sum(x['matched_cpu']['outcome']==k for x in pairs) for k in ['win','tie','loss']},
        'versus_initial_winner_counts':{k:sum(x['versus_initial_winner_equal_sweeps']['outcome']==k for x in pairs) for k in ['win','tie','loss']},
        'mean_gain_per_site':statistics.mean(x['equal_sweeps']['gain']/x['case']['L'] for x in pairs),
        'search_and_test_optimizer_cpu_seconds':sum(r['cpu_seconds'] for r in dev+data),
        'search_and_test_optimizer_wall_seconds':sum(r['wall_seconds'] for r in dev+data),
        'verification_wall_seconds':sum(r['verification_seconds'] for r in dev+data),
        'attempts':len(dev)+len(data),'saved_states':sum(len(r['history']) for r in dev+data),
        'disclosure':'Same agent as harness author; prepared environment; not a blinded independent contributor test; all trial attempts recorded.'}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
