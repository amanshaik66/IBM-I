# IBM i experimental unknowns

These questions require authoritative documentation review and a real, fingerprinted LPAR; the blueprint does not answer them from memory.

* Exact supported source forms, compiler products/options and target-release compatibility on candidate 7.4/7.5/7.6 environments.
* Object-name/library templates that satisfy ten-character limits without collisions at projected scale.
* Precise activation-group lifetime, service-program signature and state behavior for chosen build options.
* DDS multi-format, member, override, access-path maintenance and native-lock observations across planned interactions.
* Commitment definitions and journaling requirements when DDS native I/O and SQL participate in one transaction.
* Lock-wait/deadlock diagnostics, job states and safe deterministic contention timing.
* DTAQ capacity, timeout, ordering and damaged/unavailable resource behavior for installed facilities.
* Message propagation, inquiry routing, reply handling, MSGW and QSYSOPR behavior under selected job descriptions.
* SBMJOB routing, scheduling, job log retention, spool identity and subsystem/prestart/autostart behavior.
* Adopted-authority, AUTL, profile/group and IFS authority observations under least-privilege personas.
* CCSID conversion for source, jobs, database fields, IFS streams, spool and each integration adapter.
* Available IBM i SQL Services and fidelity of object/job/lock/message/spool inspection.
* Installed MQ, Connect:Direct, Java, compilers and other licensed products; simulators cannot establish their product semantics.
* Feasible object provenance hashes for each object type and save/restore effects on identity.
* Safe resource-pressure tests permitted on the development partition.
