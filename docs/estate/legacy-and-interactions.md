# Controlled legacy realism and interaction architecture

RES intentionally remains difficult to collect and modernize, but every hazard is registered rather than accidental.

* Stable accounting files are shared by old RPG, COBOL batch and new SQL views; ownership and allowed write paths are documented.
* DTAARAs hold business date, deployment generation and small switches; global state is read through wrappers except designated legacy programs.
* Library-list resolution, OVRDBF, member selection and unqualified calls drive historical variants. Alternate deployment libraries create discoverable shadow objects.
* Dynamic calls and constructed object names are sourced from validated configuration, with a registry of possible targets. Apparently dead targets remain marked dynamically reachable.
* Generated copybooks, DDS and programs retain generator inputs/version and generated provenance. Near-duplicates model branch acquisitions but have an explicit convergence plan.
* Source-less vendor programs live in `RESVEND`, expose recorded interfaces/messages/side effects, and are black boxes in dependency graphs.
* Deprecated code is retained only when referenced by a case, rollback generation or dynamic target. Truly dead code is labeled and never silently deleted.

Natural interaction clusters include:

1. Customer/account native lookup: CHAIN + composite key + LF/access path + OVRDBF + member + library list + locks + multiple jobs.
2. Payment posting: SQLRPGLE + native account access + journaling + commitment + rollback + DTAQ + ledger worker + duplicate correlation.
3. EOD: CLLE + SBMJOB + JOBD/JOBQ/SBSD/routing + status/escape/inquiry messages + MSGW + restart + PRTF/spool/OUTQ.
4. 5250 service: DSPF/subfile/indicators + RPG program + ILE service procedures + SQL/native I/O + authority + message subfile.
5. Partner intake: IFS authority + SFTP contract + CCSID conversion + QShell/PASE + multi-member staging + COBOL parse + SQL validation + archive.
6. Versioned service: modules + service program + BNDDIR/binder signatures + activation groups + static/dynamic calls + deployment library switching.

Obscure semantics that cannot fit without distortion are assigned `semantic_edge`, still use leased RES test resources, and must document why no business/operations placement is honest.
