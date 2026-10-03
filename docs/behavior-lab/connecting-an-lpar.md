# Connecting a real IBM i development LPAR

1. Provision a non-production profile with least privilege and dedicated library/IFS prefixes; define cleanup and retention policy.
2. Copy `manifests/environment.example.json`, set a stable environment ID and release, and select capability adapters. Put hostnames and secret *references* in deployment-local configuration; inject credentials from environment or a secret manager.
3. Implement and review adapters for the minimum capabilities. Typically SSH/SFTP handles commands/files and ODBC/JDBC handles SQL; do not force all operations through either.
4. Run a read-only probe to capture release, CCSID, PTF/toolchain information and clock. Registration must reject a mismatch with declared configuration.
5. Exercise workspace creation/cleanup with a synthetic connectivity check. Then run one semantic case at a time under the centralized library lease.
6. Store raw job logs, compiler listings, commands, hashes and observations. Evidence becomes authoritative only after policy validation confirms a real adapter and environment registration.

Open questions to calibrate on the target include installed licensed programs/compiler levels, naming/CCSID conventions, SQL service availability, job-log retention, spool export, authority design, and reliable inspection APIs. Nothing in the current repository answers these experimentally.

## Registration and discovery gate

Registration first captures an environment fingerprint: release, TR/PTFs, partition/system identity, architecture, relevant licensed products and compilers, Db2/SQL Services, CCSID/locale/timezone/language and formats, selected system/job/profile values, library list, work-management context, and feature flags. Unknown values remain explicit `null`/`unknown`; they are never inferred. The canonical fingerprint SHA-256 is bound into every authoritative evidence package.

Discovery then emits individual capability records. Scheduling compares these records with the case requirements before allocating isolation leases. `unavailable`, `blocked`, and `requires_configuration` stop or defer execution without producing a semantic FAIL. A read-only discovery implementation and reviewed redaction rules are prerequisites for the first connection.
