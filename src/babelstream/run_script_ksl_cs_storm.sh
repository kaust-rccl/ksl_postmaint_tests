#!/bin/bash --login


nodename=${SLURM_NODELIST} # This works because we always run on a single node

arraysize=$(( 1024*1024*1024 )) # Must be multiple of 1024

stdout="STDOUT.${nodename}"
/bin/rm ${stdout}

for device in $(seq 0 3); do

    echo -e "\nUsing device: ${device}\n" | tee -a ${stdout}
    ./bin/cuda-stream --device ${device} --arraysize ${arraysize} | tee -a ${stdout}

done

# Calculate the per-node total for Triad
awk '/Triad/ {T=T+$2} END{printf "\nTriad(node) %11.3f MB/s\n",T}' ${stdout}
