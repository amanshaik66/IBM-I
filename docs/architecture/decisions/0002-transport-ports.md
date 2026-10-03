# ADR 0002: Capability-oriented transport ports

**Status:** Accepted

The controller depends on typed capability protocols rather than SSH, JDBC, or vendor implementations. A configured environment maps capabilities to adapters, allowing composition. Adapter authority is fixed by implementation. This avoids assuming one channel can faithfully expose every IBM i facility.
