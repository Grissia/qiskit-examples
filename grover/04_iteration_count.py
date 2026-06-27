#!/usr/bin/env python
"""Compare Grover results with different iteration counts.

Goal: show that more Grover iterations are not always better. After the target
state is amplified, additional iterations rotate amplitude away from it.
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from matplotlib import pyplot as plt


SHOTS = 10_000
TARGET = "0100"


def mark_state(qc: QuantumCircuit, target: str) -> None:
    for qubit, bit in enumerate(reversed(target)):
        if bit == "0":
            qc.x(qubit)

    qc.h(3)
    qc.mcx([0, 1, 2], 3)
    qc.h(3)

    for qubit, bit in enumerate(reversed(target)):
        if bit == "0":
            qc.x(qubit)


def apply_diffusion(qc: QuantumCircuit) -> None:
    qc.h(range(4))
    qc.x(range(4))

    qc.h(3)
    qc.mcx([0, 1, 2], 3)
    qc.h(3)

    qc.x(range(4))
    qc.h(range(4))


def build_circuit(iterations: int) -> QuantumCircuit:
    qc = QuantumCircuit(4, 4)

    # ======================
    # Initial superposition
    # ======================

    qc.h(range(4))

    for _ in range(iterations):
        # ======================
        # Oracle: mark |0100>
        # ======================

        mark_state(qc, TARGET)

        # ======================
        # Diffusion operator
        # ======================

        apply_diffusion(qc)

    # ======================
    # Measurement
    # ======================

    qc.measure(range(4), range(4))
    return qc


def main() -> None:
    sim = AerSimulator()
    all_counts = {}

    for iterations in range(1, 6):
        qc = build_circuit(iterations)
        result = sim.run(qc, shots=SHOTS).result()
        counts = result.get_counts()
        all_counts[f"{iterations} iteration(s)"] = counts

        target_hits = counts.get(TARGET, 0)
        print(f"{iterations} iteration(s): {counts}")
        print(f"Target probability: {target_hits / SHOTS:.3f}\n")

    plot_histogram(all_counts)
    plt.show()


if __name__ == "__main__":
    main()
