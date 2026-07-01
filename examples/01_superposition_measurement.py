#!/usr/bin/env python
"""Create a two-qubit superposition and compare state before/after measurement."""

from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

from qiskit_examples.simulation import create_simulator


def build_circuit() -> QuantumCircuit:
    qr = QuantumRegister(2, name="q")
    cr = ClassicalRegister(2, name="c")
    circuit = QuantumCircuit(qr, cr)

    circuit.h(qr)
    circuit.save_statevector(label="before_measurement")
    circuit.measure(qr, cr)
    circuit.save_statevector(label="after_measurement")
    return circuit


def main() -> None:
    circuit = build_circuit()
    simulator = create_simulator()
    result = simulator.run(circuit, shots=10_000).result()
    data = result.data()

    print("--- Circuit ---")
    print(circuit)
    print("\n--- Counts ---")
    print(result.get_counts())
    print("\n--- Statevector before measurement ---")
    print(data["before_measurement"].draw(output="text"))
    print("\n--- Statevector after measurement ---")
    print(data["after_measurement"].draw(output="text"))


if __name__ == "__main__":
    main()
