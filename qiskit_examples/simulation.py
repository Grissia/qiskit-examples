"""Simulator helpers for concise examples and tests."""

from __future__ import annotations

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def run_counts(circuit: QuantumCircuit, shots: int = 10_000) -> dict[str, int]:
    """Run a circuit on AerSimulator and return measurement counts."""
    simulator = AerSimulator()
    result = simulator.run(circuit, shots=shots).result()
    return result.get_counts()
