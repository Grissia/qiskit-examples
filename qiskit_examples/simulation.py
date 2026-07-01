"""Simulator helpers for concise examples and tests."""

from __future__ import annotations

import os

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def simulator_device() -> str | None:
    """Return the requested Aer device from the environment, if any."""
    device = os.environ.get("QISKIT_AER_DEVICE", "").strip()
    return device or None


def create_simulator() -> AerSimulator:
    """Create an AerSimulator, optionally forcing CPU or GPU."""
    device = simulator_device()
    if device is None:
        return AerSimulator()
    return AerSimulator(device=device)


def run_counts(circuit: QuantumCircuit, shots: int = 10_000) -> dict[str, int]:
    """Run a circuit on AerSimulator and return measurement counts."""
    simulator = create_simulator()
    result = simulator.run(circuit, shots=shots).result()
    return result.get_counts()
