"""Recompute comparisons from recorded independently verified checkpoints."""
import json
from fractions import Fraction
from pathlib import Path
import statistics
from qground.evaluator import case_by_id

ROOT=Path('results/pilot')

def best(items):
    return min(items,key=lambda x: x['energy'])

def comparison(b,c):
    blo,bhi=map(Fraction,b['energy_interval']);clo,chi=map(Fraction,c['energy_interval'])
    return {'gain':b['energy']-c['energy'], 'gain_interval':[str(blo-chi),str(bhi-clo)],
            'outcome':'win' if blo-chi>Fraction(1,10**10) else ('loss' if bhi-clo < -Fraction(1,10**10) else 'tie'),
            'baseline_witness':b['witness'],'candidate_witness':c['witness']}

def main():
    rows=json.loads((ROOT/'heldout.json').read_text())
    comparisons=[]
    for b in [r for r in rows if r['run_label']=='baseline']:
        c=next(r for r in rows if r['run_label']=='selected' and r['instance']==b['instance'] and r['seed']==b['seed'])
        a=next(r for r in rows if r['run_label']=='aa' and r['instance']==b['instance'] and r['seed']==b['seed'])
        budget=min(b['cpu_seconds'],c['cpu_seconds'])
        baseline=[h for h in b['history'] if h['cpu_seconds']<=budget]
        candidate=[h for h in c['history'] if h['cpu_seconds']<=budget]
        matched=comparison(best(baseline),best(candidate)) if baseline and candidate else {'outcome':'insufficient checkpoints'}
        comparisons.append({'instance':b['instance'],'seed':b['seed'],
            'equal_sweeps':comparison(b,c),'common_cpu_seconds':budget,'matched_cpu':matched,
            'cpu_ratio_candidate_over_baseline':c['cpu_seconds']/b['cpu_seconds'],
            'aa_energy_difference':a['energy']-b['energy'],
            'aa_cpu_ratio':a['cpu_seconds']/b['cpu_seconds']})
    summary={'selected':json.loads((ROOT/'selection.json').read_text())['selected'],
        'pairs':comparisons,
        'equal_sweep_counts':{k:sum(c['equal_sweeps']['outcome']==k for c in comparisons) for k in ['win','tie','loss']},
        'matched_cpu_counts':{k:sum(c['matched_cpu']['outcome']==k for c in comparisons) for k in ['win','tie','loss']},
        'mean_gain_per_site_equal_sweeps':statistics.mean(c['equal_sweeps']['gain']/case_by_id(c['instance'])['L'] for c in comparisons),
        'mean_gain_per_site_matched_cpu':statistics.mean(c['matched_cpu']['gain']/case_by_id(c['instance'])['L'] for c in comparisons if 'gain' in c['matched_cpu']),
        'median_cpu_ratio':statistics.median(c['cpu_ratio_candidate_over_baseline'] for c in comparisons),
        'max_aa_energy_difference':max(abs(c['aa_energy_difference']) for c in comparisons),
        'aa_cpu_ratio_range':[min(c['aa_cpu_ratio'] for c in comparisons),max(c['aa_cpu_ratio'] for c in comparisons)],
        'limitations':['Three public, frozen held-out Hamiltonians; no population-level inference.',
                      'Two seeds are repeated runs for deterministic methods, not independent Hamiltonian samples.',
                      'Other workloads were present; wall-time speedup claims are unsupported.',
                      'CPU matching uses best completed sweep at common per-pair ceiling; unused remainder is below one next sweep.',
                      'Variants are established methods; novelty is not claimed.']}
    (ROOT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    allrows=json.loads((ROOT/'dev.json').read_text())+rows
    frontier=[]
    for name in sorted({r['instance'] for r in allrows}):
        r=best([r for r in allrows if r['instance']==name])
        c=case_by_id(name)
        lower=-(Fraction(c['delta'])+2)/4*(Fraction(c['J1'])*(c['L']-1)+Fraction(c['J2'])*(c['L']-2))
        if c['J2']=='0.5' and c['delta']=='1': lower=Fraction(-3*c['L'],8)
        frontier.append({'instance':name,'energy':r['energy_interval'][1],
            'energy_interval':r['energy_interval'],'proven_lower_bound':str(lower),
            'method':r['method'],'witness':r['witness'],'witness_sha256':r['witness_sha256'],
            'by':'local pilot (TeNPy DMRG)', 'source':'results/pilot/'+('dev.json' if c['split']=='dev' else 'heldout.json'),
            'updated':'2026-10-20'})
    Path('discover/records.json').write_text(json.dumps(frontier,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
