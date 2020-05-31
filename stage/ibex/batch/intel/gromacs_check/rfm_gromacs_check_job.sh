#!/bin/bash
#SBATCH --job-name="rfm_gromacs_check_job"
#SBATCH --ntasks=8
#SBATCH --ntasks-per-node=8
#SBATCH --output=rfm_gromacs_check_job.out
#SBATCH --error=rfm_gromacs_check_job.err
#SBATCH --time=0:30:0
#SBATCH --partition=batch
module load intelstack-default
module load gromacs/2019.4/openmpi-2.1.1-intel-2018-sp
export OMP_NUM_THREADS=1
mpirun -np 8 gmx_mpi mdrun -deffnm md_0_1
