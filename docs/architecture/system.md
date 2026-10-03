# Foundation architecture

## Boundaries

The coverage registry defines *what observable behavior is claimed*. The estate provides one business context, platform sources provide implementation, the Behavior Lab performs operations and captures observations, and evidence records provenance. These boundaries keep future collection and differential comparison deterministic without building the Modernizer here.

The controller is a local control plane, not a distributed scheduler. A future centralized scheduler owns LPAR capacity, library leases, limits, and dependency-aware ordering. Workers use isolated Git worktrees and one semantic-case contract each. Integration gates validate the registry and require independent review.

## Data flow

A case plus environment configuration produces an execution plan. A capability router selects one or more transports. The runner creates a collision-resistant library, uploads sources, records before-state, compiles and executes, captures after-state and artifacts, compares observable values, cleans up, then emits an immutable evidence package. Secrets enter through environment variables or an external secret provider and are never serialized.

## Trust boundary

`Transport.authority` is intrinsic to the adapter, not caller-controlled. Mock authority is always `non_authoritative`. The evidence policy rejects trusted status and all IBM i verification transitions unless evidence identifies a registered real environment, source revision/hashes, commands and artifacts. Offline validation does not establish platform semantics.

## RES module model

Common owns identifiers, messages, shared records, and cross-domain services. Customers manages parties; Accounts balances and account lifecycle; Orders commercial intent; Payments posting and notification; Accounting journals/ledgers; Reporting statements; Operations batch, queues, operator interaction and recovery. Dependencies flow through declared contracts and Common, not direct file coupling. Future domains extend the manifest without changing registry schema.
