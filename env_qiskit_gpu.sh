#!/usr/bin/env bash

CONDA_ENV_NAME="${CONDA_ENV_NAME:-qiskit-gpu}"
LOCAL_CONDA_PREFIX="$(pwd)/.miniforge3"

if command -v module >/dev/null 2>&1; then
    module purge
    module load cuda/12.8
    module load python/3.11
fi

if [ -f "$LOCAL_CONDA_PREFIX/etc/profile.d/conda.sh" ]; then
    . "$LOCAL_CONDA_PREFIX/etc/profile.d/conda.sh"
elif command -v conda >/dev/null 2>&1; then
    CONDA_BASE=$(conda info --base)
    . "$CONDA_BASE/etc/profile.d/conda.sh"
fi

if command -v conda >/dev/null 2>&1; then
    conda activate "$CONDA_ENV_NAME"
fi

SITE=$(python -c 'import site; print(site.getsitepackages()[0])')
CUDA_LD_LIBRARY_PATH="$SITE/nvidia/nvjitlink/lib"
CUDA_LD_LIBRARY_PATH="$CUDA_LD_LIBRARY_PATH:$SITE/nvidia/cusparse/lib"
CUDA_LD_LIBRARY_PATH="$CUDA_LD_LIBRARY_PATH:$SITE/nvidia/cublas/lib"
CUDA_LD_LIBRARY_PATH="$CUDA_LD_LIBRARY_PATH:$SITE/nvidia/cusolver/lib"
CUDA_LD_LIBRARY_PATH="$CUDA_LD_LIBRARY_PATH:$SITE/nvidia/cuda_runtime/lib"
export LD_LIBRARY_PATH="$CUDA_LD_LIBRARY_PATH${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export QISKIT_AER_DEVICE=GPU

echo "===== Qiskit GPU environment loaded ====="
echo "Python: $(command -v python)"
echo "CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-}"
echo "CONDA_DEFAULT_ENV=${CONDA_DEFAULT_ENV:-}"
echo "QISKIT_AER_DEVICE=$QISKIT_AER_DEVICE"
