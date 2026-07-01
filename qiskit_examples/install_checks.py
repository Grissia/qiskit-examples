"""Pre-install checks for supported Qiskit example environments."""

from __future__ import annotations

import sys


GPU_PYTHON_VERSION = (3, 11)


def check_gpu_python() -> int:
    current = sys.version_info[:2]
    if current == GPU_PYTHON_VERSION:
        return 0

    expected = ".".join(str(part) for part in GPU_PYTHON_VERSION)
    actual = ".".join(str(part) for part in current)
    print(
        "ERROR: GPU install is pinned to the debug.log-proven wheel set and "
        f"requires Python {expected}. Current Python is {actual}: {sys.executable}",
        file=sys.stderr,
    )
    print(
        "Create/activate a Python 3.11 environment first, then run "
        "`make install-gpu` again.",
        file=sys.stderr,
    )
    return 1


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "gpu":
        return check_gpu_python()

    print("usage: python -m qiskit_examples.install_checks gpu", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
