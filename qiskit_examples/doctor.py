"""Print local environment details relevant to Qiskit Aer."""

from __future__ import annotations

import importlib.metadata as metadata
import os
import platform
import shutil
import subprocess
import sys


PACKAGES = (
    "qiskit",
    "qiskit-aer",
    "qiskit-aer-gpu",
    "qiskit-aer-gpu-cu11",
    "qiskit-terra",
)


def package_version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "NOT INSTALLED"


def main() -> int:
    print("host:", platform.node() or "unknown")
    print("python:", sys.executable)
    print("python_version:", platform.python_version())
    print("CUDA_VISIBLE_DEVICES:", os.environ.get("CUDA_VISIBLE_DEVICES", ""))
    print("QISKIT_AER_DEVICE:", os.environ.get("QISKIT_AER_DEVICE", ""))

    for package in PACKAGES:
        print(f"{package}: {package_version(package)}")

    nvidia_smi = shutil.which("nvidia-smi")
    if nvidia_smi is None:
        print("nvidia-smi: NOT FOUND")
        return 0

    print("nvidia-smi:", nvidia_smi)
    subprocess.run([nvidia_smi], check=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
