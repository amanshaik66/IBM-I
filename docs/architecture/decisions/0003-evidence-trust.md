# ADR 0003: Evidence-gated verification

**Status:** Accepted

Platform verification states require authoritative evidence from a registered real IBM i environment. Mock and offline results are explicitly non-authoritative and cannot be promoted. Evidence is append-only, content-addressable where practical, and retains expected and observed values for later differential comparison.
