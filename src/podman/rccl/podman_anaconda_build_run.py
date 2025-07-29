#!/usr/bin/env python3

import os
import subprocess
import socket
import sys

# Add BUILDAH_ISOLATION=chroot to env
# Run `source vars.sh` before running this script

# Define isolated root/runroot
TMPROOT = "/tmp/podman_root"
TMPRUN = "/tmp/podman_run"

env = os.environ.copy()
DOCKERFILE_PATH = "Dockerfiles/ANACONDA/Dockerfile"
IMAGE_TAG = "anaconda:test"

def run(cmd, success_msg=None, check=True, **kwargs):
    try:
        print(f"🛠️  Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=check, **kwargs)
        if success_msg:
            print(f"✅ {success_msg}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {' '.join(cmd)}")
        sys.exit(1)

def main():
    print(f"\nRunning Docker build test on host: {socket.gethostname()}")
    print(f"Podman root      = {TMPROOT}")
    print(f"Podman runroot   = {TMPRUN}\n")
    print(f"Isolation        = {env['BUILDAH_ISOLATION']}\n")    
    
    # Step 1: Build image
    run([
        "podman", "--root", TMPROOT, "--runroot", TMPRUN,
        "build", "-t", IMAGE_TAG, "-f", DOCKERFILE_PATH
    ], success_msg="Built Docker image")

    # Step 2: Test python + mpich availability
    test_script = (
        "which python && python --version && "
        "which mpicc && mpicc -v || echo 'MPICH not found'"
    )

    print("\n🚀 Launching container to test Python and MPICH...\n")

    run([
        "podman", "--root", TMPROOT, "--runroot", TMPRUN, 
        "run", "--rm", IMAGE_TAG,
        "bash", "-c", test_script
    ], success_msg="Container test complete")

if __name__ == "__main__":
    main()

