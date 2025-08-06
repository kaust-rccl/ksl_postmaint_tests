#!/usr/bin/env python3

import os
import subprocess
import socket
import getpass

# 1) Extend PATH for personal installs
os.environ["PATH"] = f"{os.path.expanduser('~')}/.local/bin:" + os.environ["PATH"]

username = getpass.getuser()

# Use per-user directory under /ibex/users
BASE_DIR = f"/ibex/scratch/{username}/podman_test"
WEKA_ROOT = os.path.join(BASE_DIR, "root")
WEKA_RUN = os.path.join(BASE_DIR, "run")

# Create necessary directories
os.makedirs(WEKA_RUN, exist_ok=True)

# 3) Diagnostics
hostname = socket.gethostname()
print(f"\n Job is running on: {hostname}")
print(f" Podman root      = {WEKA_ROOT}")
print(f" Podman runroot   = {WEKA_RUN}")

# Check filesystem type (should show 'weka' in Type column if WekaFS)
try:
    df_output = subprocess.check_output(["df", "-T", BASE_DIR], text=True)
    print("Filesystem check (expecting 'weka'):")
    print(df_output.strip().splitlines()[-1])
except subprocess.CalledProcessError as e:
    print("❌ Failed to run `df -T`:", e)

# 4) Run Podman container
podman_cmd = [
    "podman",
    "--root", WEKA_ROOT,
    "--runroot", WEKA_RUN,
    "run", "--rm",
    "docker.io/library/hello-world"
]

print("\n🚀 Launching Podman container...\n")

try:
    subprocess.run(podman_cmd, check=True)
    print("\n✅ SUCCESS: Podman ran hello-world container.")
except subprocess.CalledProcessError as e:
    print("\n❌ Podman container failed.")
    print(e)
except FileNotFoundError:
    print("\n❌ Podman binary not found. Is it in your $PATH or module loaded?")

