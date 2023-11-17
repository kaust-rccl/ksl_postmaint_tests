#!/bin/bash
HOST=`/bin/uname -n 2> /dev/null`
echo "Hostname"
hostname 

echo "Slurm Version"
sinfo -V 

echo "Operating system version"
cat /etc/redhat-release

echo "Kernel version:"
uname -r

echo "LibC version:"
rpm -q glibc

echo "CPU and HT/SMT:"
lscpu

echo "RAM"
free -m 

echo "Mellanox OFED"
ofed_info -n

echo " IB adapters and firmware:"
ibstat

echo " Local storage:"
lsblk
df -h

echo " GPFS:"
rpm -q gpfs.base

echo " Lustre:"
cat /sys/fs/lustre/version
echo "Weka"
weka version
echo" BeeGFS:"
beegfs-ctl | grep -i version

if [[  $HOST == *gpu* ]]
 then
     echo" NVIDIA driver/kernel module:"
     nvidia-smi
     echo" CUDA version"
     echo $CUDA_VERSION
fi
echo "Job status:"
scontrol show job $SLURM_JOB_ID






