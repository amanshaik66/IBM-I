# Source, configuration, and security standards

IBM i source names must be uppercase, at most ten characters before the conventional extension, and live under `ibmi/<language>/<module>/`. Every source header states `UNVERIFIED ON IBM i` until authoritative evidence exists. Configuration contains secret references only. Logs redact credentials. Setup and cleanup are idempotent; tests operate only in leased RES-prefixed libraries and IFS roots.
