# Runner isolation review

Superseded configuration: at the scientist's request, agent internet access was restored to `public`. The no-network checks below describe the earlier configuration, not the current agent policy. The verifier remains offline.

Reviewed 2026-11-16. Status: partially verified; instructor frontier runner unavailable.

## Verified

- `.github/workflows/validate.yml` invokes `tools/validate.sh`, which pins Harbor 0.23.0 and runs only oracle and nop. No frontier model was run.
- Inspected cached Harbor 0.23.0 package source (distribution metadata confirmed version). `trial/network_policy.py` resolves the task environment baseline and agent/verifier phase policies. Executed the actual resolver against the current task with default trial configuration: all four policies are `no-network` with empty host allowlists.
- `trial/trial.py` wraps agent execution in `_phase_network_policy`. Docker enforcement uses an egress-control sidecar and `network-policy deny-all` for NO_NETWORK; absence of required enforcement support raises an error rather than silently allowing public access.
- Default agent mounts are trial log/artifact directories, not the task repository. `environment/Dockerfile` copies only input data. Separate verifier context is tests/. Oracle answer upload is intentionally different from a normal solver run.
- Earlier direct Docker smoke check used the task agent image with `--network none`: input and NumPy/SciPy available, `/solution`, `/tests`, `/authoring` absent, outbound TCP to 1.1.1.1:443 blocked with errno 101. That check is not a live Harbor enforcement test.

## Not verified

The instructor's frontier-agent launch command/configuration is absent from this checkout. No running evaluation containers were present during inspection. Consequently the deployed runner version, effective mounts, phase policies, external tools and model proxy are unknown. No live Harbor trial was launched in this review.

Harbor supports run-level `extra_allowed_hosts` for environment and agent configuration; these widen a no-network policy to an allowlist. Additional environment mounts and extra compose files can also alter isolation. Task-authored explicit compose networking is respected by this version. The current task has no compose override, and the CI command supplies no such overrides. This does not establish what the instructor supplies.

## Required deployment checks

Obtain the instructor launch command/config, exact Harbor version and agent implementation. Confirm effective policies, allowlists, extra compose files and mounts. Inspect actual containers and egress policy during the agent phase; probe outbound HTTP/TCP and absence of answer files there. Do not rely only on Docker NetworkMode: Harbor may enforce deny-all using a network sidecar. Ensure model access cannot proxy arbitrary downloads and no host-side browser/web tool bypasses container controls. Use fresh trial log/artifact directories and no prior answer-bearing trajectory. Retain sanitized inspection/probe results with the evaluated run.

Conclusion: the checked-in CI configuration and pinned policy resolver honor the task isolation setting with default options. Actual frontier evaluation isolation remains unverified pending access to its runner configuration/runtime.
