"""JSON Schema adapter with a dependency-free subset for bootstrap environments.

CI installs ``jsonschema`` and uses the full Draft 2020-12 implementation. The fallback
covers every keyword used by this repository so validation remains runnable offline.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from typing import Any

__all__ = ["Draft202012Validator", "FormatChecker"]

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # pragma: no cover - selected only in minimal bootstrap images
    FormatChecker = None

    @dataclass
    class _Error:
        path: tuple[str | int, ...]
        message: str

    class Draft202012Validator:  # type: ignore[no-redef]
        def __init__(self, schema: dict[str, Any], format_checker: Any = None) -> None:
            self.schema = schema

        def iter_errors(self, value: Any) -> Iterator[_Error]:
            yield from _check(self.schema, value, ())


def _check(schema: dict[str, Any], value: Any, path: tuple[str | int, ...]) -> Iterator[Any]:
    expected = schema.get("type")
    types = expected if isinstance(expected, list) else [expected] if expected else []
    mapping = {
        "object": dict,
        "array": list,
        "string": str,
        "integer": int,
        "boolean": bool,
        "null": type(None),
    }
    if types and not any(
        isinstance(value, mapping[t]) and not (t == "integer" and isinstance(value, bool))
        for t in types
    ):
        yield _Error(path, f"expected type {expected}")
        return
    if "const" in schema and value != schema["const"]:
        yield _Error(path, f"must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        yield _Error(path, f"must be one of {schema['enum']!r}")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            yield _Error(path, "string is too short")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            yield _Error(path, f"does not match {schema['pattern']}")
        if schema.get("format") == "date-time":
            try:
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                yield _Error(path, "invalid date-time")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            yield _Error(path, "array has too few items")
        if schema.get("uniqueItems") and len({repr(item) for item in value}) != len(value):
            yield _Error(path, "array items are not unique")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                yield from _check(item_schema, item, path + (index,))
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                yield _Error(path, f"missing required property {key}")
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, item in value.items():
            if key in properties:
                yield from _check(properties[key], item, path + (key,))
            elif isinstance(additional, dict):
                yield from _check(additional, item, path + (key,))
            elif additional is False:
                yield _Error(path + (key,), "additional property is not allowed")
