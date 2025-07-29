#!/usr/bin/env python3

import os
import subprocess
import socket
import getpass

# 1) Extend PATH for personal installs
os.environ["PATH"] = f"{os.path.expanduser('~')}/.local/bin:" + os.environ["PATH"]

username = getpass.getuser()

# Use per-user directory under /ibex/users
BASE_DIR = f"/tmp/podman_test"
XFS_ROOT = os.path.join(BASE_DIR, "root")
XFS_RUN = os.path.join(BASE_DIR, "run")

# Create necessary directories
os.makedirs(XFS_RUN, exist_ok=True)

# 3) Diagnostics
hostname = socket.gethostname()
print(f"\n Job is running on: {hostname}")
print(f" Podman root      = {XFS_ROOT}")
print(f" Podman runroot   = {XFS_RUN}")

# Check filesystem type (should show 'xfs' in Type column if XFS)
try:
    df_output = subprocess.check_output(["df", "-T", BASE_DIR], text=True)
    print("Filesystem check (expecting 'xfs'):")
    print(df_output.strip().splitlines()[-1])
except subprocess.CalledProcessError as e:
    print("❌ Failed to run `df -T`:", e)

# 4) Run Podman container
podman_cmd = [
    "podman",
    "--root", XFS_ROOT,
    "--runroot", XFS_RUN,
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

