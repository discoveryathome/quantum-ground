# Public demo concept

“Find a better arrangement of a quantum magnet.” Nearby spins and next-nearby
spins favor correlations that compete. A contributor chooses a representation
and a way to improve it. The same frozen puzzle and memory limit apply to everyone.
A verifier checks the full proposed state and certifies its energy.

The public score should show **energy improved over the best frozen baseline
at the same compute budget**, together with a visible certificate badge and
replay link. Do not show ordinary DMRG's first-to-sixth-sweep descent as if it
were an agent beating the research frontier. Distinguish three levels:

1. Solver learning curve: the fixed algorithm improves a starting state.
2. Contributor gain: a changed method beats the strong baseline under the rules.
3. Scientific advance: an independently validated result beyond relevant prior
   art. This pilot does not establish level 3.

A 32-spin unrestricted state has 2^32 amplitudes. The proposed MPS stores only
thousands of real numbers, at the cost of restricting which states it can
represent. That is a compelling, accurate explanation of the representation
challenge. It is not evidence of quantum hardware advantage or a complete
simulation of every possible 32-spin state.

Suggested demo: draw the chain with nearest and next-nearest links, then show
baseline and contributor energy traces, the fixed bond cap, counted CPU work,
and the exact decimal enclosure. An expandable note explains why the upper
bound is certified but the true minimum is generally unknown. Keep a solved
dimer control as a tutorial, clearly marked as known science.

If the observed contributor improvement is only tiny last-decimal movement,
say that plainly. A magnified axis should display its scale and the absolute
gain. A visual demo cannot repair weak scientific headroom. Do not promise
that every donated session will find an improvement.
