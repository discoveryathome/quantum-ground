# Operations and provenance

This task is local to `start-quantum-ground/`. The git repository is `project/`;
protocol fetches, the optional verified helper, the audited shallow TeNPy clone,
package cache and later clean-checkout test are in the same task folder.
At the end of the original LOCAL trial, no remote had been created and no push
or public post had occurred. No user credentials were read and no donor preset
or user application setting changed. A later owner request authorized GitHub
publication and a hub registry PR; see docs/REVIEW.md for the current status.

Free disk before installation: approximately 33 GiB. Initial environment and
source footprint: 242 MiB, below the protocol's 2 GiB approval threshold.
Hardware: arm64 Mac14,2; 24 GiB RAM; eight logical CPUs. Numerical libraries are
restricted to one thread. The interpreter is CPython 3.13.0; package versions
are in requirements.lock and loaded BLAS metadata is in results/qa/numerical-runtime.json.

The pinned TeNPy v1.1.0 source commit is
3c3304e2a7a1b90a9cd983c095da6678b9e7d2b1. The source was screened before use,
with no findings; setup.py was inspected. Installation used prebuilt wheels,
no compilation, no sudo and no global package changes. The official macOS
arm64 CPython 3.13 TeNPy wheel SHA-256 is
220c1a2b57d7b9ce2a6bca0135c5dd643182b173d039cc826e065cfec0e7564b
(from the PyPI release JSON retained in the task's protocol directory).
The pilot's screen report is protocol/screen.json.

On macOS scripts/cpu.sh uses sandbox-exec to deny network and filesystem writes
outside the checkout (except /dev/null). A checkout-local TMPDIR supports tests.
The profile allows reads, so this is not a complete confidentiality boundary.
Computation only runs the authored pilot and screened pinned dependencies.
On other operating systems use an external execution sandbox; the wrapper
alone only restricts numerical threads there.

Other CPU-heavy user workloads were observed during the session. Do not infer
uncontended performance or wall-time speedup from these measurements. Paired
process CPU times, A/A repeats, numerical iteration counts and sweep caps are
recorded to make the limitation inspectable. Scientific energy certificates
do not depend on these timing conditions.

Two setup failures preceded the valid initial development dataset: TeNPy
mutated nested option dictionaries into non-JSON Config objects; a single-site
intermediate export needed canonicalization. Both were fixed and the entire
initial development phase restarted. Failed directories are preserved outside
versioned results, with logs in results/failed-dev-*.log. They are excluded from
scientific comparisons. The exact verifier caught the export problem; a
regression test now covers every single-site checkpoint.

Final task footprint, including both virtual environments, source, witnesses and
cache: approximately 540 MiB. Fresh-checkout verification is documented in QA.md.
