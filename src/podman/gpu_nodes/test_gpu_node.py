#!/usr/bin/env python3

import os
import subprocess
import socket

# Temporary directories for Podman storage
TMPROOT = "/tmp/podman_root"
TMPRUN = "/tmp/podman_run"

# Ensure required directories exist
os.makedirs(TMPROOT, exist_ok=True)
os.makedirs(TMPRUN, exist_ok=True)

# Print where we're running
hostname = socket.gethostname()
print(f"\n🚀 Running nvidia-smi inside container on {hostname}\n")

# Define Podman run command
podman_cmd = [
    "podman",
    "--root", TMPROOT,
    "--runroot", TMPRUN,
    "run", "--rm",
    "--device", "nvidia.com/gpu=all",
    "docker.io/nvidia/cuda:12.4.1-base-ubuntu22.04",
    "nvidia-smi"
]

# Run Podman command
try:
    subprocess.run(podman_cmd, check=True)
    print("\n✅ SUCCESS: nvidia-smi ran successfully inside the container.")
except subprocess.CalledProcessError as e:
    print("\n❌ Podman container failed to run.")
    print(e)
except FileNotFoundError:
    print("\n❌ Podman binary not found. Is it in your $PATH or module loaded?")

