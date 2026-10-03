# ADR 0007: DAG builds and provenance-preserving dependency graphs

**Status:** Accepted

Build nodes declare prerequisites explicitly; directory order is never build order. Compile context is language-sensitive optional metadata. Source-less/vendor objects are explicit black boxes with known interfaces. Dependency edges preserve discovery source, confidence, dynamic resolution, and unresolved targets.
