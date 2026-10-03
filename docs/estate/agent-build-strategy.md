# Agent decomposition for building one estate

The planner selects one workflow slice, one owned component boundary, and normally one semantic case. A generated task contract names the workflow ID, component ID, capability IDs, semantic ID, build-DAG nodes, data fixtures, allowed paths, dependency prerequisites, isolation, expected business outcome and evidence gate.

Good task: “Implement `customer-keyed-lookup` in component `RES-CUST-QUERY` for `RES-WF-CUST-0002`, satisfying `IBMSEM-RPG-CHAIN-0001`; add its build node, dependency edges, deterministic customer fixture and observable results.” Bad task: “Add CHAIN examples.”

Units are small but vertically traceable:

1. reserve workflow/component/semantic ownership;
2. satisfy prerequisite DAG nodes;
3. implement one shared-application behavior;
4. update allocation and bidirectional traceability without redefining semantics;
5. add deterministic setup/cleanup and tests;
6. run static gates;
7. schedule the LPAR independently;
8. obtain verifier and reviewer approval.

Parallel agents must not invent libraries, entities, messages or interfaces outside catalogs. Architectural changes are separate governance tasks. Integration agents assemble only reviewed units and never weaken expected results. Domain owners sequence shared contracts before consumers; schema/database migrations serialize on owned objects. Semantic-edge tasks must justify their classification and must not add artificial production dependencies.
