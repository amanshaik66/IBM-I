# Security, documents and integration architecture

## Security model

Human and service identities map to application roles separately from IBM i profiles. Groups represent customer service, payments, finance, operations, security administration, audit and integration. Authorization lists protect domain data/object sets. Libraries default to least privilege; public authority is explicit. IFS trees have service-group ownership and restrictive inbound/outbound/archive permissions.

Normal users may inquire or perform bounded maintenance. Payment approval, ledger adjustment, period close, spool release, replay and security administration require distinct roles and separation of duties. Adopted authority is confined to reviewed command/program gateways that perform one privileged action, drop authority at the boundary and emit audit records. Tests include low-authority denial, group inheritance, ownership, private authority, authorization-list changes, adopted authority and application-level denial. Credentials never enter source, catalogs or evidence.

## IFS and document topology

`/res/<environment>/inbound/<partner>`, `work/<execution>`, `outbound/<partner>`, `archive/<business-date>`, `reports`, `config-public` and leased test namespaces have separate authorities and retention. Intake lands into a temporary name, validates size/hash/encoding/schema, quarantines malformed input, then atomically promotes it. Formats include CSV, fixed-width, XML, JSON and binary envelopes. QShell/PASE performs checksum, archive/compression, naming and controlled conversion; application parsers retain original bytes and declared CCSID. Exports use manifests, sequence/correlation, acknowledgements and archive reconciliation.

## Integration topology

| Counterparty | IBM i side | Contract side |
|---|---|---|
| payment network | MQ request/reply and async events | deterministic authorization/return scripts |
| customer portal | Java REST plus prestart service jobs | HTTP requests, auth claims, scripted responses |
| legacy partner | SOAP/XML service | WSDL-shaped request/response contract |
| bank/warehouse | SFTP and FTPS fixed/CSV files | landing, acknowledgement and rejection scripts |
| clearing house | Connect:Direct/NDM transfer contract | process/name/status simulation |
| market data | C socket client/server | framed deterministic feed and disconnects |
| notifications | SMTP | captured mail envelope/body and failures |
| analytics/partner DB | JDBC/ODBC and external database adapter | deterministic datasets and transaction contract |

IBM i behavior under test includes programs, jobs, commands, CCSID conversion, sockets, files, authorities, queues, transactions and error handling. External product internals are outside scope; simulators preserve only observable contracts, correlation, latency, timeout and failures. Real adapters and simulators share interface contracts but evidence identifies which endpoint ran.
