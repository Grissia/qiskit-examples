#!/usr/bin/env python
"""Five-qubit Grover search for one marked state: |01100>."""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from matplotlib import pyplot as plt


SHOTS = 10_000
TARGET = "01100"
ITERATIONS = 4


def mark_state(qc: QuantumCircuit, target: str) -> None:
    """Apply a phase flip to one target state.

    The target string uses Qiskit's counts order. For five qubits, a printed
    state is q4 q3 q2 q1 q0.
    """
    for qubit, bit in enumerate(reversed(target)):
        if bit == "0":
            qc.x(qubit)

    qc.h(4)
    qc.mcx([0, 1, 2, 3], 4)
    qc.h(4)

    for qubit, bit in enumerate(reversed(target)):
        if bit == "0":
            qc.x(qubit)


def apply_diffusion(qc: QuantumCircuit) -> None:
    """Apply the standard Grover diffusion operator to all five qubits."""
    qc.h(range(5))
    qc.x(range(5))

    qc.h(4)
    qc.mcx([0, 1, 2, 3], 4)
    qc.h(4)

    qc.x(range(5))
    qc.h(range(5))


def build_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(5, 5)

    # ======================
    # Initial superposition
    # ======================

    qc.h(range(5))

    for _ in range(ITERATIONS):
        # ======================
        # Oracle: mark |01100>
        # ======================

        mark_state(qc, TARGET)

        # ======================
        # Diffusion operator
        # ======================

        apply_diffusion(qc)

    # ======================
    # Measurement
    # ======================

    qc.measure(range(5), range(5))
    return qc


def main() -> None:
    qc = build_circuit()
    sim = AerSimulator()
    result = sim.run(qc, shots=SHOTS).result()
    counts = result.get_counts()

    print("Counts:", counts)
    print(qc)
    plot_histogram(counts)
    plt.show()


if __name__ == "__main__":
    main()
