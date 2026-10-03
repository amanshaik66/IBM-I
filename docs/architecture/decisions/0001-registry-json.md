# ADR 0001: JSON Schema and JSON registry records

**Status:** Accepted

Use one JSON document per semantic case, validated by versioned JSON Schema. JSON provides deterministic parsing and broad tooling. IDs are immutable; schema versions evolve compatibly, while registry records can be partitioned indefinitely. YAML may be generated for presentation but is not authoritative.
