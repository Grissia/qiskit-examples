# Qiskit Examples

This repository is a small Qiskit teaching project. It starts with basic
superposition and measurement, then builds toward half adders and Grover search
oracles.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
make install
```

## Lessons

| Lesson | Script | Topic |
| --- | --- | --- |
| 1 | `examples/01_superposition_measurement.py` | Hadamard gates, measurement, and statevectors |
| 2 | `examples/02_half_adder.py` | XOR, AND, CNOT, and Toffoli gates |
| 3 | `grover/README.md` | Five Grover search lessons |

Run a lesson with `make`:

```bash
make run-superposition
make run-half-adder
make run-grover-two-qubit
make run-grover-five-qubit
make run-grover-constraints
make run-grover-iterations
make run-grover-multiple
```

Run the test suite:

```bash
make test
```

## Notes for Learners

Qiskit prints measurement bit strings in classical-bit order, with the highest
classical bit on the left. The Grover scripts in `grover/` use that same
convention, so a target such as `0100` refers to the printed counts key `0100`.

The examples intentionally keep circuits small enough to inspect in terminal
output. Larger circuits should move repeated oracle logic into named helper
functions and should be tested with probabilistic assertions rather than exact
shot counts.
