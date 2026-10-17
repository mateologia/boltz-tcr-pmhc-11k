#!/bin/bash
#SBATCH --job-name=boltz-all-gpu
#SBATCH --partition=gpu0
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --output=slurm-all-gpu-%j.out
#SBATCH --error=slurm-all-gpu-%j.err

cd $SLURM_SUBMIT_DIR

# 1. Carregamento do ambiente Conda
source ~/miniconda3/etc/profile.d/conda.sh
conda activate boltz_env

# 2. Direcionar estritamente para a GPU 0 e ativar kernels CUDA
export CUDA_VISIBLE_DEVICES=0
export BOLTZ_USE_KERNELS=1

# 3. Threads de CPU leves
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export MKL_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_DYNAMIC=FALSE

# 4. Gerenciamento de memória PyTorch
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

echo "=== Iniciando lote de 11.000 complexos na GPU em $(date) ==="
echo "Node alocado: $SLURMD_NODENAME"
nvidia-smi

# 5. Execução em GPU blindada nos núcleos 17 a 20 apontando para a pasta com 11.000 YAMLs
taskset -c 17-20 boltz predict ~/boltz_inputs_all/ \
    --use_msa_server \
    --accelerator gpu \
    --devices 1 \
    --num_workers 2 \
    --diffusion_samples 1 \
    --recycling_steps 1 \
    --sampling_steps 25 \
    --cache ~/.boltz \
    --override \
    --out_dir boltz_results_all_gpu

echo "=== Predição finalizada em $(date) ==="
