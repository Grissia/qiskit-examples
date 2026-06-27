# Grover Search Notes

This folder collects five Grover examples. The code is intentionally written as
small scripts with visible circuit steps, because the goal is to learn the
algorithm rather than hide the details behind a framework.

Qiskit prints measurement results with the highest classical bit on the left.
For example, if a circuit measures q0, q1, q2, q3 into c0, c1, c2, c3, a printed
key such as `0100` means `c3 c2 c1 c0 = 0100`. In these examples the target
strings are written in the same order as Qiskit's printed counts.

Grover's algorithm has three repeating parts:

1. Create a uniform superposition with Hadamard gates.
2. Use an Oracle to give valid states a negative phase.
3. Use the diffusion operator to amplify the marked states.

The approximate number of iterations is:

```text
R ~= (pi / 4) * sqrt(N / M)
```

`N` is the size of the search space and `M` is the number of marked states.

## 1. Two-qubit Grover Search

Script: `01_two_qubit_search.py`

This is the smallest useful Grover search example. With two qubits, the search
space has four states:

```text
|00>, |01>, |10>, |11>
```

The example searches for `|10>`. Since `N = 4` and `M = 1`, the ideal iteration
count is approximately:

```text
(pi / 4) * sqrt(4 / 1) ~= 1.57
```

For this tiny circuit, one Oracle plus one diffusion step is enough to make the
target state dominate the measurement result.

The Oracle is built by turning `|10>` into `|11>`, applying a controlled-Z phase
flip, and then restoring the qubit that was temporarily inverted. This pattern
is useful: convert the target state into the all-ones state, phase flip it, then
undo the conversion.

Run it:

```bash
python grover/01_two_qubit_search.py
```

## 2. Five-qubit Grover Search

Script: `02_five_qubit_search.py`

This example searches for one target in a five-qubit search space. The target is
`|01100>`, so the search space contains:

```text
N = 2^5 = 32
M = 1
```

The approximate iteration count is:

```text
(pi / 4) * sqrt(32 / 1) ~= 4.44
```

The script uses 4 iterations. Each iteration applies:

1. Oracle: mark `|01100>` with a negative phase.
2. Diffusion: amplify the marked state's amplitude.

The Oracle uses the same target-to-all-ones trick as the two-qubit example. For
every `0` in the target string, apply `X` before the multi-controlled operation.
After the phase flip, apply the same `X` gates again to restore the basis.

## 3. Constraint Oracle

Script: `03_constraint_oracle.py`

This example solves a logical constraint problem with Grover's algorithm. There
are four binary variables:

```text
v0, v1, v2, v3
```

The valid solution must satisfy all constraints:

```text
v0 != v1
v2 != v3
v0 != v2
v1 != v3
```

The important point is that the code does not hardcode the two valid bitstrings.
Instead, the Oracle is constructed from the logic of the problem.

The qubit layout is:

```text
q0-q3 : search qubits representing v0-v3
q4-q7 : ancilla qubits for intermediate XOR computations
q8    : phase output qubit
```

The search qubits start in a uniform superposition:

```text
H on q0-q3
```

The output qubit is prepared as `|->`:

```text
X
H
```

The Oracle computes four XOR conditions into ancilla qubits:

```text
c0 = v0 XOR v1
c1 = v2 XOR v3
c2 = v0 XOR v2
c3 = v1 XOR v3
```

For binary variables, `a != b` is exactly `a XOR b = 1`. So a candidate state is
valid only when all four ancilla qubits are `1`.

After computing the constraints, the circuit applies:

```text
MCX([c0, c1, c2, c3], out)
```

Because `out` is in `|->`, this produces a phase flip on every state satisfying
all constraints. Then the circuit uncomputes the ancilla qubits by reversing the
CNOT operations. This is necessary because the diffusion operator should act on
a clean search register, not on search qubits entangled with temporary work
qubits.

The search space has:

```text
N = 2^4 = 16
M = 2
```

So the iteration count is:

```text
(pi / 4) * sqrt(16 / 2) ~= 2.22
```

The script runs exactly 2 iterations, then measures only q0-q3. Ancilla and
output qubits are not measured because they are implementation details of the
Oracle.

## 4. Changing the Number of Grover Iterations

Script: `04_iteration_count.py`

This example shows that more Grover iterations are not always better.

Grover's algorithm can be understood as rotating amplitude toward the marked
state. The first few iterations increase the target probability, but after the
best point, extra iterations rotate amplitude away from the target. That is why
the iteration count matters.

The script searches for `|0100>` in a four-qubit search space and runs the same
circuit with 1, 2, 3, 4, and 5 iterations. It prints the target probability for
each run. You should see the target probability rise near the best iteration
count and then fall again.

This is also why the formula uses `M`, the number of marked states:

```text
R ~= (pi / 4) * sqrt(N / M)
```

The algorithm is powerful, but it is not improved by blindly adding more
Oracle/diffusion rounds.

## 5. Multiple Marked States

Script: `05_multiple_marked_states.py`

Earlier examples usually assume there is only one target state. Grover's
algorithm does not require that. The Oracle can mark multiple valid states.

For example, a two-qubit Oracle could mark both:

```text
|01> and |10>
```

That means both states receive a negative phase. The diffusion operator does not
need to know which state was marked. It amplifies all marked states together.

This script uses five qubits and marks:

```text
|01100> and |10000>
```

Both targets become negative-phase states during the Oracle step. After
diffusion, measurement may return either valid state. The exact count split will
vary because the simulator samples probabilistically.

When there are multiple marked states, the iteration formula becomes:

```text
R ~= (pi / 4) * sqrt(N / M)
```

Here:

```text
N = 2^5 = 32
M = 2
```

So:

```text
(pi / 4) * sqrt(32 / 2) ~= 3.14
```

The script uses 3 iterations.

The key lesson is that more targets means fewer iterations. With many marked
states, the algorithm has less work to do because a random measurement already
has a higher chance of landing on a valid state.

## Running All Grover Examples

From the repository root:

```bash
make run-grover-two-qubit
make run-grover-five-qubit
make run-grover-constraints
make run-grover-iterations
make run-grover-multiple
```

Each script prints counts and displays a histogram.
