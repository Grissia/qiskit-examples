PYTHON ?= python
PIP ?= $(PYTHON) -m pip
ENV = PYTHONPATH=.

.PHONY: install install-gpu doctor check-gpu run-superposition run-half-adder run-grover-two-qubit run-grover-five-qubit run-grover-constraints run-grover-iterations run-grover-multiple test clean

install:
	$(PIP) install -r requirements.txt

install-gpu:
	$(ENV) $(PYTHON) -m qiskit_examples.install_checks gpu
	$(PIP) uninstall -y qiskit qiskit-aer qiskit-aer-gpu qiskit-aer-gpu-cu11 qiskit-terra
	$(PIP) install --no-cache-dir -r requirements-gpu.txt

doctor:
	$(ENV) $(PYTHON) -m qiskit_examples.doctor

check-gpu:
	$(ENV) $(PYTHON) -m qiskit_examples.check_gpu

run-superposition:
	$(ENV) $(PYTHON) examples/01_superposition_measurement.py

run-half-adder:
	$(ENV) $(PYTHON) examples/02_half_adder.py

run-grover-two-qubit:
	$(ENV) $(PYTHON) grover/01_two_qubit_search.py

run-grover-five-qubit:
	$(ENV) $(PYTHON) grover/02_five_qubit_search.py

run-grover-constraints:
	$(ENV) $(PYTHON) grover/03_constraint_oracle.py

run-grover-iterations:
	$(ENV) $(PYTHON) grover/04_iteration_count.py

run-grover-multiple:
	$(ENV) $(PYTHON) grover/05_multiple_marked_states.py

test:
	$(ENV) $(PYTHON) -m pytest

clean:
	find . -type d \( -name "__pycache__" -o -name ".pytest_cache" \) -prune -exec rm -rf {} +
