#!/bin/bash

HOST=`/bin/uname -n 2> /dev/null`

echo "Hostname:"
hostname

echo "SLURM:"
sinfo -V

echo "OS:"
cat /etc/redhat-release
lsb_release -a

echo "Kernel:"
uname -a

echo "LibC:"
rpm -q glibc

echo "CPU and HT/SMT:"
lscpu

echo "RAM:"
free -m

echo "OFED:"
ofed_info -n

echo "IB adapters and firmware:"
ibstat

echo "File Systems:"
lsblk
df -h

echo "Lustre:"
cat /sys/fs/lustre/version

echo "Weka:"
weka version

if [[  $HOST == *gpu* ]]; then
     echo "NVIDIA driver/kernel module:"
     nvidia-smi
     echo "CUDA version:"
     echo $CUDA_VERSION
     echo "VBIOS:"; nvidia-smi -a | grep VBIOS
fi

echo "Job status:"
scontrol show job $SLURM_JOB_ID

echo ""

# The END #
