#!/bin/bash -l
#SBATCH -t 01:00:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=16
#SBATCH --ntasks-per-socket=8
#SBATCH --mem=65536


#module load default-appstack

module load openfoam/7.0/gnu-6.4.0

# generating mesh
mpirun -n 1 blockMesh
# partioning mesh
mpirun -n 1 decomposePar
# running on 2 nodes x 16 cores = 32 cores
#time mpirun -n 16 --ntasks-per-node=16 --ntasks-per-socket=8 --hint=nomultithread icoFoam -parallel
time srun -n 32 icoFoam -parallel


