# ADR 0006: Content-addressed artifacts and baselines

**Status:** Accepted

Evidence metadata references large immutable artifacts by SHA-256. A baseline binds semantic version, commit, fingerprint hash, evidence hash, and comparison-policy hash. Hash changes invalidate applicability. Local development uses a filesystem store; production storage may replace it without changing locators or trust rules.
