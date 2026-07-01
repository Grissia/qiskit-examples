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

## GPU Mode

Use the GPU environment helper before running GPU examples:

```bash
source env_qiskit_gpu.sh
make check-gpu
make run-grover-constraints
```

`make check-gpu` should end with:

```text
OK: Qiskit Aer GPU backend is available.
```

If you need to create the GPU environment from scratch, use Python 3.11 and
install the GPU requirements:

```bash
python -m venv .venv
source .venv/bin/activate
make install-gpu
source env_qiskit_gpu.sh
make check-gpu
```

On an HPC environment with modules, load Python and CUDA first:

```bash
module load cuda/12.8
module load python/3.11
python -m venv .venv
source .venv/bin/activate
make install-gpu
source env_qiskit_gpu.sh
make check-gpu
make run-grover-constraints
```

To run the test suite on CPU while the GPU environment is active:

```bash
QISKIT_AER_DEVICE=CPU make test
```

See `docs/gpu-development.md` for version pins, WSL notes, and troubleshooting.

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
