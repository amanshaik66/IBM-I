# IBM i Reference Enterprise System (RES)

RES is the foundation for **one coherent fictional IBM i enterprise estate** used to research documented, reproducible, application-visible behavior. It is not a syntax gallery, a claim of complete coverage, or the IBM i Modernizer. Semantic cases are integrated into business workflows spanning Common, Customers, Accounts, Orders, Payments, Accounting, Reporting, and Operations.

> **Verification boundary:** no IBM i system was available for this foundation build. All IBM i fixtures and semantics are **UNVERIFIED ON IBM i**. Offline checks prove repository consistency only; mock runs can never produce authoritative IBM i evidence.

## Architecture at a glance

* `registry/` is the machine-readable authority: extensible semantic cases, releases, JSON Schemas, and the status state machine.
* `estate/` and `docs/estate/` describe the single, multi-generation RES business application; machine-readable components, workflows, capabilities, allocations, and traceability live under `registry/estate/`, `registry/capabilities/`, and `registry/traceability/`; `ibmi/` will contain its deployable platform sources, grouped by language rather than isolated demos.
* `controller/behavior_lab/` is a typed, transport-neutral controller. Capability-oriented transports may combine SSH/SFTP, SQL, APIs, and remote calls.
* `agents/` contains narrowly scoped, one-case task contracts and safety policy.
* `tests/` contains offline unit/static tests now and semantic/integration/concurrency/recovery suites later.
* Durable evidence is schema-controlled and authoritative only when a non-mock registered IBM i environment and provenance checks satisfy the trust policy.

See the [complete RES application blueprint](docs/estate/README.md), [system architecture](docs/architecture/system.md), [foundation hardening review](docs/architecture/foundation-hardening.md), [verification governance](docs/architecture/verification-governance.md), [roadmap](docs/architecture/roadmap.md), and the ADRs in `docs/architecture/decisions/`.

## Developer workflow

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
res-validate all
res-validate report
res-validate estate-report
pytest
ruff check .
mypy
```

The validation command can target `registry`, `tasks`, `manifests`, `architecture`, `estate`, or `all`; `estate-report` emits allocation gaps and counts. It validates schemas, immutable ID format/uniqueness, references, fixture paths, status consistency, and the prohibition on trusted mock evidence.

## Adding one semantic case

1. Reserve one immutable `IBMSEM-<DOMAIN>-<FEATURE>-<NNNN>` ID; never recycle it.
2. Create exactly one task contract from `agents/templates/task-contract.json` in an isolated branch/worktree.
3. Follow `docs/agents/one-case-workflow.md`; change only contract-approved directories.
4. Add concise references rather than copied IBM documentation and record uncertainties as `requires_investigation`.
5. Run `res-validate all` and the test suite. Offline success permits at most `statically_validated`.
6. Submit independent review. IBM i states require evidence from a registered real environment.

## Current scope and next milestone

The ten starter records demonstrate the semantic layer only. The application blueprint defines 37 shared-estate components and 23 initial workflows; those plans are not implemented IBM i functionality. The recommended next task is to connect a dedicated development LPAR through a first real transport adapter, register it without secrets, and compile/execute these ten cases one by one to produce authoritative evidence. No bulk case generation should start before that feedback loop is proven.

Licensed under the terms in [LICENSE](LICENSE).
