# Foundation hardening review

## Gaps found

The original foundation had no complete environment fingerprint, capability-to-case scheduling decision, DAG build description, object provenance, dependency-edge provenance, multi-dimensional isolation declaration, operational recovery contracts, external artifact store, explicit comparison policies, baseline binding, semantic-definition history, or runtime observation schema. Evidence embedded job logs, case expectations lacked governance, source-less objects and compiler context were not representable, and coverage output could not expose its separate dimensions. The initial library-only workspace model was insufficient for jobs, profiles, queues, spool, journals, and integrations.

## Hardened boundaries

Environment registration is configuration; a captured fingerprint is an execution fact and is content-addressed. A scheduler compares declared case requirements to discovered capabilities and returns `runnable`, `unavailable`, `blocked`, or `requires_configuration`; none is a semantic test failure. IBM i 7.4, 7.5, and 7.6 are candidate records only.

Build manifests are DAGs. Every created object receives provenance that binds source (or an explicit source-less classification), commit, manifest hash/version, compile context, environment, resulting identity, case IDs, and evidence. Dependency graphs distinguish declared, static, and runtime discovery and retain unresolved/dynamic edges rather than guessing.

Cases declare every required isolation dimension and six rerunnable lifecycle phases. Cleanup verification compares inventories and future lease recovery scans expired namespaces for orphans. Unique libraries do not isolate user profiles, jobs, QTEMP, library lists, work-management objects, queues, journals, spool, IFS paths, or partner namespaces.

Large evidence artifacts live in a write-once, content-addressed store. Evidence and baselines bind hashes; mutation invalidates verification. Baselines are release/fingerprint-specific and never assume compatibility across PTFs or releases.
