#!/usr/bin/env python
"""Grover search with multiple marked states.

This example marks both |01100> and |10000>. Measurement can return either
valid state because the Oracle gives both states a negative phase and the
diffusion operator amplifies both of them together.
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from matplotlib import pyplot as plt


SHOTS = 10_000
TARGETS = ("01100", "10000")
ITERATIONS = 3


def mark_state(qc: QuantumCircuit, target: str) -> None:
    """Apply a phase flip to one target state in Qiskit's counts order."""
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
        # Oracle: mark multiple states
        #
        # Each call creates a negative phase for one target. Calling it twice
        # means the Oracle marks both |01100> and |10000>.
        # ======================

        mark_state(qc, TARGETS[0])
        mark_state(qc, TARGETS[1])

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
