#!/usr/bin/env python
"""Grover search with an Oracle constructed from logical constraints.

There are four binary variables: v0, v1, v2, v3.

The valid solution must satisfy all constraints:

    v0 != v1
    v2 != v3
    v0 != v2
    v1 != v3

This example does not hardcode the valid bitstrings. Instead, it computes each
constraint into an ancilla qubit using XOR, then uses phase kickback to mark
the states where all constraints are true.
"""

from qiskit import QuantumCircuit

from qiskit_examples.simulation import create_simulator


SHOTS = 10_000
ITERATIONS = 2

v0, v1, v2, v3 = 0, 1, 2, 3
c0, c1, c2, c3 = 4, 5, 6, 7
out = 8


def apply_oracle(qc: QuantumCircuit) -> None:
    # ======================
    # Oracle
    #
    # Compute:
    # c0 = v0 XOR v1
    # c1 = v2 XOR v3
    # c2 = v0 XOR v2
    # c3 = v1 XOR v3
    #
    # If all c0,c1,c2,c3 are 1, the state satisfies every "!=" constraint.
    # The output qubit starts in |->, so MCX creates a phase flip by phase
    # kickback instead of storing a visible 0/1 answer.
    # ======================

    qc.cx(v0, c0)
    qc.cx(v1, c0)

    qc.cx(v2, c1)
    qc.cx(v3, c1)

    qc.cx(v0, c2)
    qc.cx(v2, c2)

    qc.cx(v1, c3)
    qc.cx(v3, c3)

    qc.mcx([c0, c1, c2, c3], out)

    # ======================
    # Uncompute
    #
    # Reverse every CNOT used above so the ancilla qubits return to |0>.
    # This keeps the search register clean before the diffusion operator.
    # ======================

    qc.cx(v3, c3)
    qc.cx(v1, c3)

    qc.cx(v2, c2)
    qc.cx(v0, c2)

    qc.cx(v3, c1)
    qc.cx(v2, c1)

    qc.cx(v1, c0)
    qc.cx(v0, c0)


def apply_diffusion(qc: QuantumCircuit) -> None:
    # ======================
    # Diffusion operator
    #
    # Apply inversion about the mean only to q0-q3, because q4-q7 are ancilla
    # qubits and q8 is the phase output qubit.
    # ======================

    qc.h(v0)
    qc.h(v1)
    qc.h(v2)
    qc.h(v3)

    qc.x(v0)
    qc.x(v1)
    qc.x(v2)
    qc.x(v3)

    qc.h(v3)
    qc.mcx([v0, v1, v2], v3)
    qc.h(v3)

    qc.x(v0)
    qc.x(v1)
    qc.x(v2)
    qc.x(v3)

    qc.h(v0)
    qc.h(v1)
    qc.h(v2)
    qc.h(v3)


def build_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(9, 4)

    # ======================
    # Initial superposition
    # ======================

    qc.h(v0)
    qc.h(v1)
    qc.h(v2)
    qc.h(v3)

    # Prepare the output qubit in |->.
    qc.x(out)
    qc.h(out)

    for _ in range(ITERATIONS):
        apply_oracle(qc)
        apply_diffusion(qc)

    # ======================
    # Measurement
    #
    # Measure only the four search qubits. Ancilla and output qubits are part
    # of the Oracle machinery, not the final answer.
    # ======================

    qc.measure(v0, 0)
    qc.measure(v1, 1)
    qc.measure(v2, 2)
    qc.measure(v3, 3)
    return qc


def main() -> None:
    qc = build_circuit()
    sim = create_simulator()
    result = sim.run(qc, shots=SHOTS).result()
    counts = result.get_counts()

    print("Counts:", counts)
    print(qc)


if __name__ == "__main__":
    main()
