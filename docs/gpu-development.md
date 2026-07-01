# GPU Development Notes

This file is for maintainers and local environment debugging. User-facing setup
instructions live in `README.md`.

## Version Set

The GPU environment is pinned to the combination that works with Qiskit Aer GPU:

```text
Python 3.11
qiskit==1.4.5
qiskit-aer-gpu==0.15.1
```

Python 3.14 does not work with `qiskit-aer-gpu==0.15.1`; pip will report that no
matching distribution exists.

## Local WSL Notes

This repository can use a local Miniforge install at `.miniforge3`. The helper
script activates the `qiskit-gpu` conda environment by default:

```bash
source env_qiskit_gpu.sh
```

The helper sets `QISKIT_AER_DEVICE=GPU` and prepends the pip-installed NVIDIA
CUDA libraries to `LD_LIBRARY_PATH`.

`make check-gpu` intentionally does more than list Aer devices. It also runs a
small GPU circuit, because `available_devices: ('CPU', 'GPU')` only proves that
the installed Aer wheel has GPU support. It does not prove that CUDA execution
can create a device context.

## WSL GPU Diagnostics

If `make check-gpu` fails with `No CUDA device available`, check WSL device
visibility:

```bash
ls -l /dev/dxg
nvidia-smi
```

In restricted tool sandboxes, `/dev/dxg` may be hidden even when the normal WSL
terminal can use the GPU. In that case, run GPU checks from a normal terminal.

You can also test the CUDA driver directly:

```bash
source env_qiskit_gpu.sh
python - <<'PY'
import ctypes

cuda = ctypes.CDLL("libcuda.so.1")
cuInit = cuda.cuInit
cuInit.argtypes = [ctypes.c_uint]
cuInit.restype = ctypes.c_int

count = ctypes.c_int()
cuDeviceGetCount = cuda.cuDeviceGetCount
cuDeviceGetCount.argtypes = [ctypes.POINTER(ctypes.c_int)]
cuDeviceGetCount.restype = ctypes.c_int

print("cuInit:", cuInit(0))
print("cuDeviceGetCount:", cuDeviceGetCount(ctypes.byref(count)), count.value)
PY
```

CUDA error code `100` means `CUDA_ERROR_NO_DEVICE`.

## HPC Notes

On the HPC environment from `debug.log`, use the module-provided CUDA and
Python first:

```bash
module load cuda/12.8
module load python/3.11
```

If the conda environment is named `qiskit-examples`, activate it with:

```bash
CONDA_ENV_NAME=qiskit-examples source env_qiskit_gpu.sh
```

The important dynamic-library fix is to put the pip-installed NVIDIA libraries
before system CUDA libraries in `LD_LIBRARY_PATH`.

## Useful Commands

```bash
make doctor
make check-gpu
QISKIT_AER_DEVICE=CPU make test
```
