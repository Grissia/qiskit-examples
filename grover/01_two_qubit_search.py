#!/usr/bin/env python
"""Two-qubit Grover search.

Goal: search for |10> in a four-state search space:

    |00>, |01>, |10>, |11>

Qiskit prints measured bitstrings as q1 q0 for this two-qubit circuit, so the
target string "10" means q1=1 and q0=0.
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from matplotlib import pyplot as plt


SHOTS = 10_000
TARGET = "10"


def build_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(2, 2)

    # ======================
    # Initial superposition
    # ======================

    qc.h(0)
    qc.h(1)

    # ======================
    # Oracle: mark |10>
    #
    # Qiskit counts order: q1 q0.
    # |10> means q1=1, q0=0.
    # Turn |10> into |11>, apply CZ, then restore q0.
    # ======================

    qc.x(0)
    qc.cz(0, 1)
    qc.x(0)

    # ======================
    # Diffusion operator
    # ======================

    qc.h(0)
    qc.h(1)

    qc.x(0)
    qc.x(1)

    qc.h(1)
    qc.cx(0, 1)
    qc.h(1)

    qc.x(0)
    qc.x(1)

    qc.h(0)
    qc.h(1)

    # ======================
    # Measurement
    # ======================

    qc.measure(0, 0)
    qc.measure(1, 1)
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
