# Local handoff

This pilot is ready for independent replication, not public intake. The author
has run the experiment; another person has not reviewed it. No maintainer has
agreed to take responsibility. The verifier and frontier need careful review;
review capacity, rather than compute supply, will set the public project pace.

Install the pinned dependencies in a local environment, then run
`./scripts/reproduce.sh` from the repository root. Allow ten minutes for the
automated part and about thirty minutes to inspect the formulation and checks.
See `docs/FEATURE_ASSESSMENT.md` for the evidence and launch recommendation.

After independent replication, the useful optimization task is to beat the
upgraded hybrid incumbent, on a newly preregistered stratified suite. The exposed
held-out cases cannot serve as fresh evidence for further adaptive tuning.
Three independent bounded contributor sessions would test sustained progress.

This is a local request, not a message sent to any person or service.

```discover
{
  "v": 0,
  "kind": "handoff",
  "task": "replication-01",
  "scope": "Independently reproduce and audit the local pilot before public intake",
  "base": "612b999649f7e918390c271c4f1a630a2e71f0b4",
  "posted_at": "2026-10-20T21:56:38.076445+00:00",
  "request": {
    "question": "Can another contributor reproduce saved energies and confirm that the checker implements the stated Hamiltonian?",
    "first_step": "./scripts/reproduce.sh",
    "success_test": "All tests, ED comparisons, exact witness checks and metadata checks pass; report any model or checker discrepancy, with no acceptance implied.",
    "track": "replication",
    "est_minutes": 30
  }
}
```
