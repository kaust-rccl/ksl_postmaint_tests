import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class Podman_checks(rfm.RunOnlyRegressionTest):
    """
    Define base class for podman tests.
    """
    variant = parameter(
        [
            "nfs",
            "wekafs",
            "tmpfs",
            "nvidia-smi_test",
            "rccl_anaconda_rebuild",
            "load_tarball",
        ]
    )
    maintainers = ["mohamed.elgharawy@kaust.edu.sa"]

    @run_after("init")
    def setting_variables(self):
        """
        Define test resources.
        """
        self.descr = "Podman functionality checks"
        self.constraint = self.variant
        self.tags = {self.variant, "podman", "singlenode"}
        # Environment settings
        self.valid_systems = ["ibex:batch"]
        self.valid_prog_environs = ["cpustack_builtin"]
        self.time_limit = "1h"
        self.prerun_cmds = ["module purge", "module load python"]
        if self.variant == "nvidia-smi_test":
            self.num_gpus_per_node = 1

        # Resource and runtime settings
        self.exclusive_access = True

        # In the run phase invoke the executable name as below
        if self.variant == "nfs":
            self.sourcesdir = "../src/podman/filesystems/nfs"
            self.executable = "python ./podman_nfs.py"
            self.sanity_patterns = sn.assert_found(
                r"SUCCESS: Podman ran hello-world container", self.stdout
            )
        elif self.variant == "wekafs":
            self.sourcesdir = "../src/podman/filesystems/weka"
            self.executable = "python ./podman_weka.py"
            self.sanity_patterns = sn.assert_found(
                r"SUCCESS: Podman ran hello-world container", self.stdout
            )
        elif self.variant == "tmpfs":
            self.sourcesdir = "../src/podman/filesystems/xfs"
            self.executable = "python ./podman_xfs.py"
            self.sanity_patterns = sn.assert_found(
                r"SUCCESS: Podman ran hello-world container", self.stdout
            )
        elif self.variant == "nvidia-smi_test":
            self.exclusive_access = False
            self.sourcesdir = "../src/podman/gpu_nodes"
            self.valid_prog_environs = ["gpustack_cuda"]
            self.executable = "python ./test_gpu_node.py"
            self.sanity_patterns = sn.assert_found(
                r"SUCCESS: nvidia-smi ran successfully inside the container",
                self.stdout,
            )
        elif self.variant == "rccl_anaconda_rebuild":
            self.sourcesdir = "../src/podman/rccl"
            self.prerun_cmds = ["module purge", "module load python", "source vars.sh"]
            self.executable = "python ./podman_anaconda_build_run.py"
            self.sanity_patterns = sn.assert_found(
                r"Container test complete", self.stdout
            )
        elif self.variant == "load_tarball":
            self.sourcesdir = "../src/podman/tarball"
            self.executable = "python ./podman_tarball.py"
            self.sanity_patterns = sn.assert_found(r"Test complete", self.stdout)

    @run_before("run")
    def set_job_options(self):
        """
        Define resource and runtime settings
        """
        self.job.options = ["--ntasks=4", "--ntasks-per-node=4", "--cpus-per-task=1"]
