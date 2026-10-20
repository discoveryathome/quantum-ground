"""Factual contributor-trial receipt, including unsuccessful and post-hoc tests."""
import json
from pathlib import Path
from datetime import datetime,timezone
P=Path('research/contributor-001')

def main():
    session=json.loads((P/'session.json').read_text())
    trial=json.loads((P/'summary.json').read_text());sup=json.loads((P/'supplement/summary.json').read_text())
    initial=json.loads(Path('results/pilot/dev.json').read_text());dev=json.loads((P/'dev.json').read_text())
    long=json.loads((P/'long-reference/run.json').read_text())
    started=datetime.fromisoformat(session['start_utc'].replace('Z','+00:00'))
    ended=datetime.fromisoformat(session['experiments_finished_at'])
    minutes=(ended-started).total_seconds()/60
    hybrid=next(r for r in dev if r['instance']=='dev24' and r['method']=='hybrid_polish')
    base=next(r for r in initial if r['instance']=='dev24' and r['method']=='baseline')
    ramp=next(r for r in initial if r['instance']=='dev24' and r['method']=='ramp')
    first=next(r for r in dev if r['instance']=='dev10' and r['method']=='hybrid_polish')
    first_minutes=(datetime.fromisoformat(first['finished_at'])-started).total_seconds()/60
    txt=['# Timed contributor trial 001','',
      f"The experiment portion lasted **{minutes:.1f} minutes**, within the requested 30–60 minute window. The first verified improvement over the initial development incumbents appeared after **{first_minutes:.1f} minutes**. Packaging and clean-checkout replay followed separately.",'',
      'This was the same agent that built the harness, using a prepared environment and existing context. It is not an independent contributor onboarding study. Early trial time included completion of the initial benchmark, literature/code inspection, hypothesis implementation and verification. No additional agent was spawned.', '',
      '## What changed','',
      'Three explicit ideas were tested: singlets along next-neighbor bonds; two sweeps near the dimer point followed by four target sweeps; and three two-site sweeps followed by three fixed-bond single-site polishing sweeps. All are grounded in existing DMRG practice. No algorithmic novelty is claimed. The last variant won development selection; its code was frozen before the fresh draw.', '',
      '| Development case | NNN singlets | Continuation | Hybrid polishing |',
      '|---|---:|---:|---:|']
    for cid in ['dev10','dev12','dev24']:
        vals=[next(r['energy'] for r in dev if r['instance']==cid and r['method']==m) for m in ['nnn_dimers','continuation','hybrid_polish']]
        txt.append('| '+cid+' | '+' | '.join(f'{v:.12f}' for v in vals)+' |')
    txt += ['',f"On dev24, polishing reduced energy by {base['energy']-hybrid['energy']:.8g} J1 versus the original baseline and {ramp['energy']-hybrid['energy']:.8g} J1 versus the previous ramp incumbent. Same chi<=8, same six sweeps. The 24-sweep ordinary baseline's best saved energy was {long['best']['energy']:.12f}, still {long['best']['energy']-hybrid['energy']:.8g} J1 above the six-sweep hybrid state. This is evidence against merely spending more sweeps on that particular baseline; it is not proof that reasoning beats every automated search strategy.", '',
      '## Primary fresh test: retained null result','',
      'The recorded OS seed independently replayed to J2=0.5, delta=1.25 at all three sizes (16,20,32). This is a known exactly dimerized line. All final-energy comparisons tied at the 1e-10 J1 decision threshold, including common-CPU comparisons. These cases were not discarded or silently replaced. This exposes a coverage weakness in a tiny unstratified draw. See fresh-suite.json and test.json.', '',
      '## Separate post-hoc coverage supplement','',
      'After observing the coverage problem, three coupling strata were fixed, one new case drawn per stratum, and the method was left unchanged. This is additional exploratory evidence, not the original preregistered primary test. The cases and source hashes were written before any supplemental score was measured.', '',
      '| Spins | J2 | delta | Original baseline | Hybrid | Energy reduction | Hybrid/baseline CPU |',
      '|---:|---:|---:|---:|---:|---:|---:|']
    for r in sup['pairs']:
        c=r['case'];txt.append(f"| {c['L']} | {c['J2']} | {c['delta']} | {r['baseline_energy']:.12f} | {r['candidate_energy']:.12f} | {r['equal_sweeps']['gain']:.6g} | {r['candidate_cpu_ratio']:.3f} |")
    ed=json.loads((P/'supplement/ed.json').read_text())['coverage16']['energy']
    r=sup['pairs'][0];oldgap=r['baseline_energy']-ed;newgap=r['candidate_energy']-ed
    txt += ['', 'Polishing won all three supplemental comparisons at equal sweeps, under common per-pair CPU ceilings, and against the previous development winner (ramp). Improvements are exact-interval separated, not rounding artifacts. CPU ratios alone do not establish speedup: the machine had other workloads and A/A timing variation.',
      f"For the 16-spin supplemental case, the numerical ED gap decreased from {oldgap:.8g} to {newgap:.8g} J1, an approximately {100*(oldgap-newgap)/oldgap:.2f}% reduction. This percentage uses a numerical ED reference, not a certified lower bound. No corresponding ground-energy error is known for the larger cases.",'',
      '## Accounting and reproducibility','',
      f"Initial pilot: 30 development runs and 18 held-out/control runs. Timed contributor additions: {trial['attempts']} primary/development runs, nine supplemental runs and one 24-sweep reference. There are 126 primary/development, 54 supplemental and 24 long-reference saved checkpoints; all received exact witness checks. Setup failures before the valid initial dataset are retained and described in docs/OPERATIONS.md.",
      f"Contributor primary/development optimizer CPU: {trial['search_and_test_optimizer_cpu_seconds']:.2f}s; supplement: {sup['optimizer_cpu_seconds']:.2f}s; long reference: {long['cpu_seconds']:.2f}s. Exact verification and actual wall time are recorded separately. These CPU totals are not the session duration and omit reasoning, preparation and ED.", '',
      'Run `./scripts/reproduce.sh` from the project root to check the archived result package. To rerun all 30 contributor search/test runs on the exact archived inputs, use `./scripts/cpu.sh -m scripts.replay_contributor --out results/contributor-replay`. A new output directory is required. Add `--case dev10 --method hybrid_polish` for a short positive control. The replay checks energies to 1e-9 J1 and independently verifies every new state. The original initial experiment also supports a new --out directory. Commands, inputs and timeouts are in VERIFY.json; frozen sources are in SOURCES.json.', '',
      'The original fresh draw and the post-hoc supplement must remain separately labeled in every report. Never count deterministic repeats as independent Hamiltonian samples or describe these known-method improvements as a new quantum ground-state discovery.', '',
      '## Open next questions','',
      '- Can three independent, cold-start contributors improve a stronger portfolio that already includes hybrid polishing? Why: this tests sustained contribution yield. First step: reproduce this package, freeze the upgraded baseline, and draw a new stratified suite. Blocked by: an agreed maintainer and independent reviewers.',
      '- Does adaptive switching improve genuinely harder finite chains at fixed total CPU and bond budgets? Why: the present trial establishes only one standard polishing step. First step: inspect dev24 traces and preregister a switching criterion without using existing test cases. Blocked by: a fresh benchmark version; old heldouts are now exposed.',
      '- Can another implementation audit the exact integer recurrence and witness interface? Why: the score checker is central to public trust. First step: run the rational full-vector controls, then reimplement one contraction independently. Blocked by: no technical dependency; independent contributor review remains outstanding.', '',
      'Credit: user-specified research question; Codex-assisted implementation and trial; TeNPy and algorithm sources in docs/LITERATURE.md. Evidence: author-checked, independently implemented energy scoring, no independent-person or maintainer acceptance.']
    (P/'README.md').write_text('\n'.join(txt)+'\n')
    print(f'Wrote contributor receipt: {minutes:.1f} experiment minutes')
if __name__=='__main__':main()
