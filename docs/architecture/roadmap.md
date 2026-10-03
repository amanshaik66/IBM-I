# Evidence-led roadmap

1. **Foundation (current):** schemas, ten specified examples, typed controller ports, mock tests, policies, CI. No IBM i verification.
2. **First 10 verified cases:** connect a development LPAR, implement least-privilege transports, calibrate CCSID/release/toolchain, compile and execute each case, capture signed/immutable evidence, and correct assumptions.
3. **100 cases:** deepen the existing business workflows, add dependency-aware scheduling, review ownership, repeatability runs, and release/configuration variants.
4. **1,000 cases:** broaden languages, object types and operational facilities; shard registries by taxonomy while retaining immutable IDs; establish capacity and flake management.
5. **Broad platform coverage:** systematically map authoritative documentation and reproducible facilities across supported releases; explicitly record unsupported/non-reproducible areas.
6. **Interaction testing:** cover cross-feature concurrency, failure, recovery, authority, CCSID, activation-group and work-management combinations using designed sampling.
7. **Exhaustive Reference Estate:** continuously measure gaps, retire no IDs, preserve evidence lineage, and use the coherent estate for differential testing against future independent implementations.

Coverage percentage is reported only against a versioned, explicitly bounded taxonomy—not against “all IBM i.”
