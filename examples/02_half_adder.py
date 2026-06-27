#!/usr/bin/env python
"""Quantum half adder.

q0 and q1 are the input bits. q2 stores sum = q0 XOR q1, and q3 stores
carry = q0 AND q1. The input qubits start in superposition, so one run samples
all four input combinations.
"""

from qiskit import QuantumCircuit

from qiskit_examples.simulation import run_counts


def build_circuit() -> QuantumCircuit:
    circuit = QuantumCircuit(4, 4)

    circuit.h(0)
    circuit.h(1)

    circuit.cx(0, 2)
    circuit.cx(1, 2)
    circuit.ccx(0, 1, 3)

    circuit.measure(range(4), range(4))
    return circuit


def main() -> None:
    circuit = build_circuit()
    print("--- Circuit ---")
    print(circuit)
    print("\n--- Counts ---")
    print(run_counts(circuit))


if __name__ == "__main__":
    main()
