#!/bin/bash
#Initialize conda
source /software/etc/profile.d/conda.sh
conda activate base
exec "$@"
