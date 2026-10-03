# Semantic expectation and independent verification governance

Three conceptual roles are separated in process: an **implementer** changes implementation/fixtures, a **verifier** operates the approved real-environment run, and an independent **reviewer** evaluates evidence, comparison policy, and scope. These are review roles, not repository identities.

The integration flow is: implementation branch → static gates → centrally leased IBM i execution → immutable evidence/artifacts → independent evidence review → authoritative baseline approval → integration gate. The implementer cannot be the sole authority for verification.

Expected-behavior changes are semantic changes, not implementation fixes. They require an updated semantic-definition version and rationale, `change_class: semantic_change`, authoritative evidence provenance, and independent review. Agents should not modify expectation files under an implementation-only task contract. Validation rejects a semantic-change declaration without evidence. Repository branch protection should require CODEOWNERS/review approval for `registry/coverage`, `registry/policies`, and `registry/baselines`; host enforcement remains an operator task.

A semantic change invalidates or supersedes affected baselines. Changing source, environment fingerprint, evidence package, or comparison policy hashes makes a baseline inapplicable rather than silently updating it. Comparison normalization is opt-in, path-specific, justified, and reviewed; the default policy is strict.
