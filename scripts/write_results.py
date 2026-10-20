"""Produce the factual initial-pilot report from recorded results."""
import json
from pathlib import Path
import statistics
from qground.evaluator import case_by_id
P=Path('results/pilot')

def main():
    summary=json.loads((P/'summary.json').read_text())
    dev=json.loads((P/'dev.json').read_text());held=json.loads((P/'heldout.json').read_text())
    ed={**json.loads((P/'dev-ed.json').read_text()),**json.loads((P/'heldout-ed.json').read_text())}
    counts=summary['equal_sweep_counts'];cpu=summary['matched_cpu_counts']
    text=['# Initial pilot: measured results','',
      f"The development-selected method was **{summary['selected']}**. On three held-out Hamiltonians, each run twice, it recorded **{counts['win']} wins, {counts['tie']} ties, {counts['loss']} losses** against fixed-chi two-site DMRG at six sweeps. At common per-pair CPU ceilings: **{cpu['win']} wins, {cpu['tie']} ties, {cpu['loss']} losses**.",'',
      'A win requires an exact interval separation exceeding 1e-10 J1. Two repeats of a deterministic method are not two independent Hamiltonians. These are local benchmark results, not scientific novelty or a claim of universal superiority.','',
      '| Held-out case | Baseline energy | Ramp energy | Energy reduction | Candidate/baseline CPU |',
      '|---|---:|---:|---:|---:|']
    for b in [r for r in held if r['run_label']=='baseline' and r['seed']==1729]:
        c=next(r for r in held if r['run_label']=='selected' and r['seed']==b['seed'] and r['instance']==b['instance'])
        text.append(f"| {b['instance']} | {b['energy']:.12f} | {c['energy']:.12f} | {b['energy']-c['energy']:.6g} | {c['cpu_seconds']/b['cpu_seconds']:.3f} |")
    text += ['',f"Mean held-out improvement per site: {summary['mean_gain_per_site_equal_sweeps']:.8g} J1 at equal sweeps; {summary['mean_gain_per_site_matched_cpu']:.8g} J1 at common CPU ceilings.",
      f"Largest A/A energy difference: {summary['max_aa_energy_difference']:.3g} J1. A/A CPU ratios ranged from {summary['aa_cpu_ratio_range'][0]:.3f} to {summary['aa_cpu_ratio_range'][1]:.3f}. Other machine workloads were active; wall-time speedups are not established.",'',
      '## Exact diagonalization controls','',
      '| Case | Numerical ED energy | ED residual norm | Best initial candidate minus ED |',
      '|---|---:|---:|---:|']
    for k,v in ed.items():
        e=min(r['energy'] for r in dev+held if r['instance']==k)
        text.append(f"| {k} | {v['energy']:.12f} | {v['residual_norm']:.3g} | {e-v['energy']:.6g} |")
    text += ['', 'ED operates over the full Hilbert space. Its residual is a numerical diagnostic, not a global lower-bound certificate. The isotropic J2=1/2 control additionally has the known exact bound E0=-3L/8, derived in FORMULATION.md. Small negative ED gaps at roundoff scale have no physical significance.', '',
      '## Search accounting','',
      f"The initial search contains {len(dev)} development runs and {len(held)} held-out/control runs, with six saved checkpoints per run ({6*(len(dev)+len(held))} checkpoints). All checkpoints passed independent exact-integer energy and normalization checks.",
      f"Total measured optimizer CPU: {sum(r['cpu_seconds'] for r in dev+held):.1f} s. Optimizer wall time: {sum(r['wall_seconds'] for r in dev+held):.1f} s. Separate exact verification wall time: {sum(r['verification_seconds'] for r in dev+held):.1f} s. These omit environment setup, imports, ED, failed setup attempts and agent reasoning; all such work still belongs to session cost.", '',
      'Seeds: 1729 and 2718. Source and suite hashes precede held-out evaluation in selection.json. Parameters, traces, states, A/A comparisons, CPU and wall times, Lanczos iterations and update counts are in results/pilot/. Failed pre-dataset setup attempts are described in OPERATIONS.md.', '',
      '## Interpretation and follow-up','',
      'A tighter variational upper bound is real progress on the frozen benchmark. It does not establish a new physical result, a true ground-state energy, or a generally superior algorithm. This small experiment has no confidence interval for a population of Hamiltonians. Public fixed test cases should be replaced before subsequent adaptive tuning.', '',
      'The initial method menu was not exhaustive. The timed contributor test adds structured starts, coupling continuation, and two-site-to-one-site polishing. See [the contributor report](../research/contributor-001/README.md) and [featured-pilot assessment](FEATURE_ASSESSMENT.md). The record table may include later checked contributor states on the same development instances; those do not alter this frozen initial benchmark comparison.', '',
      'Evidence level: author-checked. An independent code path checked states, but no independent contributor or maintainer has accepted them.']
    Path('docs/RESULTS.md').write_text('\n'.join(text)+'\n')
    print('Wrote docs/RESULTS.md')
if __name__=='__main__':main()
