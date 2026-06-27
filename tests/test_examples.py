from importlib import util
from pathlib import Path

from qiskit_examples.grover import dominant_states
from qiskit_examples.simulation import run_counts

ROOT = Path(__file__).resolve().parents[1]


def load_example(filename: str):
    return load_module(f"examples/{filename}")


def load_module(relative_path: str):
    path = ROOT / relative_path
    spec = util.spec_from_file_location(path.stem, path)
    module = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_half_adder_samples_all_inputs() -> None:
    module = load_example("02_half_adder.py")
    counts = run_counts(module.build_circuit(), shots=1_000)

    assert set(counts) == {"0000", "0101", "0110", "1011"}


def test_single_target_grover_amplifies_target() -> None:
    module = load_module("grover/02_five_qubit_search.py")
    counts = run_counts(module.build_circuit(), shots=1_000)

    assert max(counts, key=counts.get) == module.TARGET


def test_two_target_grover_amplifies_both_targets() -> None:
    module = load_module("grover/05_multiple_marked_states.py")
    counts = run_counts(module.build_circuit(), shots=1_000)

    assert dominant_states(counts, minimum_fraction=0.25) == set(module.TARGETS)


def test_constraint_grover_finds_expected_assignments() -> None:
    module = load_module("grover/03_constraint_oracle.py")
    counts = run_counts(module.build_circuit(), shots=1_000)

    assert dominant_states(counts, minimum_fraction=0.25) == {"0110", "1001"}
