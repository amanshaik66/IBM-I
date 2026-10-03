# Status and evidence model

The machine authority is `registry/status-machine.json`. The normal path is `specified → source_written → statically_validated → compiled_on_ibmi → executed_on_ibmi → behavior_verified_on_ibmi → integration_verified`. `blocked`, `unsupported`, and `requires_investigation` are controlled side states.

Compiled and later states require authoritative evidence. Behavior verification additionally requires a passing comparison; integration verification requires reviewed multi-case evidence. A mock can exercise controller logic but can never satisfy these guards. Status history is append-only in evidence; changing a registry status requires referencing the evidence execution ID.
