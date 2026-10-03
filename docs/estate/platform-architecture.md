# IBM i platform architecture

## Logical libraries and object resolution

Names are logical templates; final ten-character IBM i names require LPAR validation. Product code, data, and operations are deliberately separated:

| Library role | Logical name | Contents and resolution purpose |
|---|---|---|
| shared runtime | `RESCOM` | MSGF, common *SRVPGM/*MODULE, BNDDIR, commands |
| application | `RESAPP` | current domain programs, modules, DSPF/PRTF |
| legacy application | `RESLEG` | controlled older RPG/COBOL and near-duplicates |
| primary data | `RESDATA` | DDS/SQL operational files, sequences, journals |
| archive/history | `RESHIST` | history, closed periods, archived logical data |
| integration | `RESINT` | adapters, DTAQ, staging definitions, partner commands |
| operations | `RESOPS` | MSGQ, JOBQ/JOBD/SBSD definitions, run control tools |
| security | `RESSEC` | authorization lists and adopted-authority gateways |
| reporting | `RESRPT` | PRTF, report programs, output definitions |
| vendor | `RESVEND` | source-less/vendor black boxes and interface metadata |
| environment config | `RESCFGx` | environment-owned DTAARA/configuration overrides |
| deployment | `RESNEW`/`RESOLD` | controlled version switching and library-list resolution |
| test lease | `RTnnnnnn` | Behavior Lab isolated objects; never production data |
| job temporary | `QTEMP` | per-job work files, overrides and ephemeral SQL objects |

Production-style library lists place environment configuration first, then current application, legacy/vendor fallback, shared runtime, data and platform libraries. Alternate lists intentionally exercise qualified/unqualified resolution, shadow objects, version switching, missing-library failure, and dynamic calls. Overrides are scoped and always removed. Tests requiring schema/profile/queue isolation declare those dimensions separately.

Object allocation includes *LIB, *PGM, *SRVPGM, *MODULE, *FILE (PF/LF/DSPF/PRTF/save/display where applicable), *DTAARA, *DTAQ, *MSGQ, *MSGF, *CMD, *BNDDIR, *JOBD, *JOBQ, *OUTQ, *SBSD, *JRN, *JRNRCV, *AUTL and *USRPRF. User spaces cache large operational snapshots; user queues/indexes are reserved for justified high-volume lookup/monitoring experiments after IBM i validation.

## ILE topology

`RESSRV` binding directory lists common error, validation, date, decimal, audit and identifier service programs. Domain binding directories list stable domain APIs. Binder source versions exported signatures; compatible additions preserve prior signatures, and deliberate incompatible cases live only in the semantic corpus. Entry programs remain small and call service procedures through prototypes. Legacy program calls are wrapped behind gateways that translate parameter conventions and messages.

Default activation groups are avoided for modern services except where a case or legacy program requires them. Named activation groups separate interactive applications, payment posting, report generation and integration workers; caller activation groups are used only with documented lifetime expectations. Planned workflows exercise module creation, binding, imports/exports, signature checks, static and dynamic procedure/program calls, activation-group state and cleanup.

## Work management topology

| Subsystem | Work | Queues/descriptions | Behavior |
|---|---|---|---|
| `RESINTS` | 5250 interactive | workstation entries; `RESINTJD` | user library list, message subfiles, bounded priority |
| `RESBATCH` | normal batch/EOD | `RESJOBQ`, `RESBATJD` | dependency-controlled submitted jobs and restart |
| `RESPAY` | high-priority payment/accounting | `RESPAYQ`, `RESPAYJD` | limited concurrency, short transaction jobs |
| `RESRPT` | reports/statements | `RESRPTQ`, `RESRPTJD` | spool-heavy, lower priority, dedicated OUTQ |
| `RESLINK` | integration workers | `RESINTQ`, `RESINTJD` | autostart queue dispatchers and optional prestart API jobs |
| `RESLONG` | close/archive/rebuild | `RESLONGQ`, `RESLNGJD` | resource-limited long work, checkpoint required |

Routing data selects worker class; job descriptions define library list, logging, output queue and accounting code. Scheduler commands submit dependency DAG nodes, wait on job status, capture logs and distinguish held, scheduled, active, MSGW, completed and ended states. Autostart/prestart use is conditional on environment capability and will be tested rather than assumed.

## Messaging and asynchronous patterns

`RESMSGF` owns stable business and diagnostic message IDs. Domain MSGFs may extend it without duplicating common messages. Program message queues communicate completion, diagnostic and escape messages through the call stack. External `RESOPR` and domain queues receive status, notify, request and inquiry messages; only critical operational scenarios route to QSYSOPR under controlled configuration.

Patterns include payment outbox → `PAYPOSTQ` DTAQ → ledger worker; order allocation queue → inventory worker; report request queue → report worker; integration inbox DTAQ → dispatcher; and batch control DTAARA plus durable SQL run/checkpoint rows. Data areas hold small environment switches, business date and generation counters—not transaction truth. Timeouts, poison entries, duplicate delivery, queue unavailability and worker termination lead to durable exceptions and operator recovery.

## Reporting, spool and output

PRTF-backed statements, invoices, exception reports, job-control summaries and audit extracts create spool files with business correlation in user data. OUTQs separate customer output, finance-controlled output, operations, and test leases. A print router holds/releases/moves/copies output, records spool identity, exports selected artifacts to IFS, and reconciles expected report runs. Report restart must not silently duplicate customer delivery.
