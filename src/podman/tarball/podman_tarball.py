#!/usr/bin/env python3

import os
import subprocess
import socket

# Define temporary root/run directories
TMPROOT = "/tmp/podtest_root"
TMPRUN = "/tmp/podtest_run"
TARBALL = "alpine.tar"

os.makedirs(TMPROOT, exist_ok=True)
os.makedirs(TMPRUN, exist_ok=True)

hostname = socket.gethostname()
print(f"\n Running on: {hostname}")
print(f"Podman root      = {TMPROOT}")
print(f"Podman runroot   = {TMPRUN}\n")

def run_cmd(cmd, success_msg=None, fail_ok=False):
    try:
        subprocess.run(cmd, check=True)
        if success_msg:
            print(f"✅ {success_msg}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {' '.join(cmd)}")
        if not fail_ok:
            raise

# Pull the image
run_cmd(["podman", "--root", TMPROOT, "--runroot", TMPRUN, "pull", "alpine"],
        success_msg="Pulled Alpine image")

# Save the image to tarball
run_cmd(["podman", "--root", TMPROOT, "--runroot", TMPRUN, "save", "-o", "alpine.tar", "alpine"],
        success_msg="Saved Alpine image to alpine.tar")

# Remove the image
run_cmd(["podman", "--root", TMPROOT, "--runroot", TMPRUN, "rmi", "alpine"],
        success_msg="Removed Alpine image")

# Load the image back
run_cmd(["podman", "--root", TMPROOT, "--runroot", TMPRUN, "load", "-i", "alpine.tar"],
        success_msg="Reloaded Alpine image from alpine.tar")

# Run a test command
print("\nRunning container...")
run_cmd(["podman", "--root", TMPROOT, "--runroot", TMPRUN, "run", "--rm", "alpine", "echo", "Test complete"],
        success_msg="Test complete")

# Delete existing tarball to avoid modify error
if os.path.exists(TARBALL):
    os.remove(TARBALL)

