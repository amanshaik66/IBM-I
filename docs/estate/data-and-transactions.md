# Data, transaction, journaling and recovery architecture

## Storage generations

The customer/account core begins with DDS PFs and LFs because keyed native access, record formats, members and access paths are part of its history. Modern payment, order, inventory, billing and integration state uses SQL tables with constraints. Accounting deliberately mixes stable DDS ledger files, SQL views/aliases and SQL staging. New reporting uses views, indexes, functions and procedures. This coexistence creates legitimate shared contracts rather than duplicate test databases.

Representative entity groups:

* **Foundation:** enterprise, branch, currency, country, calendar, business date, number range, feature configuration, message text and audit correlation.
* **Customer:** customer, name/address/contact, relationship, status history, preference, document link and search tokens.
* **Accounts/payments:** account, product/type, balance bucket, transaction, hold, adjustment, payment instruction, authorization, posting, reversal/return, exception, reconciliation and outbox.
* **Commerce:** order/header/line/status, price/discount/tax, item, location, stock balance, reservation, movement and replenishment.
* **Billing/accounting:** invoice/line/charge/credit/application, aging bucket, collection action, chart account, journal header/line, subledger link, period, reconciliation and adjustment.
* **Trading:** trade order, execution, allocation, confirmation, settlement instruction, position and exception.
* **Operations:** batch definition/run/step/checkpoint, idempotency key, inbox/outbox, operator exception, object/run correlation, report run, transmission and audit event.

## Access patterns and database features

Customer lookup and account inquiry provide compound keys for CHAIN, SETLL/SETGT, READ/READE and reverse READP/READPE pagination. Payment/account updates provide WRITE/UPDATE/DELETE with record locks, no-lock reads and commitment control. Multi-member inbound/history PFs, aliases to selected members, OVRDBF and alternate access paths have operational purposes. Arrival-sequence audit/import files coexist with keyed LFs. Multiple-record-format logical files are limited to a documented legacy inquiry.

SQL paths include singleton SELECT, multi-row cursors, positioned updates, dynamic operational queries, procedures, scalar/table functions, identity and sequence allocation, views, indexes, aliases, check/unique/referential constraints and carefully bounded triggers. Fixtures intentionally include nullable optional data, packed/zoned decimals, currency precision, dates/times/timestamps, graphic/Unicode and multiple CCSIDs. QTEMP holds per-job selections, sort/work tables and report staging.

## Transaction boundaries

* Customer onboarding commits customer, address, audit and optional account together; external notifications use a transactional outbox.
* Payment posting commits idempotency, payment state, account transaction/balance, journal linkage and outbox atomically. Authorization calls occur before the local mutation or use a compensating state machine—never inside an indefinite database lock.
* Inventory reservation locks/checks stock and writes reservation/movement in one unit; fulfillment and shipment are later states.
* Ledger posting requires balanced debit/credit lines before commit. Period close uses checkpoints and immutable completed-period controls.
* Batch steps commit at declared restart boundaries, store high-water marks, and reconcile processed/rejected totals.

Operational files are journaled to domain journal receivers with explicit receiver management. COMMIT/ROLLBACK behavior, lock waits, interrupted jobs and recovery are authoritative only after LPAR experiments. Restart logic distinguishes safe retry, idempotent replay, compensation and manual investigation. Journal extracts support audit/reconciliation and controlled recovery tests; they are never silently used to rewrite expected results.

## Failure and recovery matrix

Missing/wrong objects and library lists fail preconditions or route controlled escape messages. Duplicate/missing records, constraints and malformed data produce business rejection or rollback according to boundary. Lock contention and carefully bounded contention cycles use short timeouts and isolated jobs. Queue timeout/full/unavailable, external outage, partial batch failure, MSGW, job termination and safe resource-pressure simulations record a durable exception and checkpoint. Cleanup verifies jobs, locks, queues, spool, journals, database rows and IFS artifacts. Destructive disk or system exhaustion is never attempted on a shared LPAR.
