"""Check whether the active Python environment can use Qiskit Aer GPU."""

from __future__ import annotations

import importlib.metadata as metadata
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
    for package in PACKAGES:
        print(f"{package}: {package_version(package)}")

    try:
        from qiskit import QuantumCircuit
        from qiskit_aer import AerSimulator
    except ModuleNotFoundError as exc:
        if exc.name not in {"qiskit", "qiskit_aer"}:
            raise
        print("ERROR: Qiskit is not installed. Run `make install-gpu` first.", file=sys.stderr)
        return 1

    simulator = AerSimulator()
    devices = simulator.available_devices()
    methods = simulator.available_methods()

    print("available_devices:", devices)
    print("available_methods:", methods)

    if "GPU" not in devices:
        print("ERROR: Qiskit Aer GPU backend is not available.", file=sys.stderr)
        return 1

    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)

    simulator = AerSimulator(device="GPU")
    try:
        simulator.run(circuit, shots=16).result()
    except RuntimeError as exc:
        print(f"ERROR: Qiskit Aer GPU backend failed to execute: {exc}", file=sys.stderr)
        return 1

    print("OK: Qiskit Aer GPU backend is available.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
