#!/usr/bin/env sh
set -eu
python -m behavior_lab.validation all --root "$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
