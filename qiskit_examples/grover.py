"""Reusable Grover search building blocks for small teaching examples."""

from __future__ import annotations

from math import floor, pi, sqrt

from qiskit import QuantumCircuit


def optimal_iterations(num_qubits: int, marked_states: int = 1) -> int:
    """Return a practical Grover iteration count for tiny examples."""
    if num_qubits < 1:
        raise ValueError("num_qubits must be positive")
    if marked_states < 1:
        raise ValueError("marked_states must be positive")
    search_space = 2**num_qubits
    if marked_states > search_space:
        raise ValueError("marked_states cannot exceed the search space")
    return max(1, floor(pi / 4 * sqrt(search_space / marked_states)))


def apply_phase_oracle(circuit: QuantumCircuit, target: str) -> None:
    """Flip the phase of one computational basis state.

    The target string uses Qiskit's printed counts order: the leftmost bit is
    the highest-index qubit. For example, target "0100" marks q3 q2 q1 q0.
    """
    num_qubits = len(target)
    if num_qubits != circuit.num_qubits:
        raise ValueError("target length must match the number of qubits")
    if set(target) - {"0", "1"}:
        raise ValueError("target must contain only 0 and 1")

    for qubit, bit in enumerate(reversed(target)):
        if bit == "0":
            circuit.x(qubit)

    circuit.h(num_qubits - 1)
    circuit.mcx(list(range(num_qubits - 1)), num_qubits - 1)
    circuit.h(num_qubits - 1)

    for qubit, bit in enumerate(reversed(target)):
        if bit == "0":
            circuit.x(qubit)


def apply_diffusion(circuit: QuantumCircuit, qubits: list[int] | range | None = None) -> None:
    """Apply the standard inversion-about-the-mean step."""
    selected = list(range(circuit.num_qubits)) if qubits is None else list(qubits)
    if not selected:
        raise ValueError("at least one qubit is required")

    circuit.h(selected)
    circuit.x(selected)

    target = selected[-1]
    controls = selected[:-1]
    circuit.h(target)
    if controls:
        circuit.mcx(controls, target)
    else:
        circuit.z(target)
    circuit.h(target)

    circuit.x(selected)
    circuit.h(selected)


def dominant_states(counts: dict[str, int], minimum_fraction: float = 0.1) -> set[str]:
    """Return states whose counts exceed a fraction of all shots."""
    total = sum(counts.values())
    return {state for state, count in counts.items() if total and count / total >= minimum_fraction}
