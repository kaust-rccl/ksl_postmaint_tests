import reframe as rfm
import reframe.utility.sanity as sn


class system_check(rfm.RunOnlyRegressionTest):
    """Define base class for system checks."""

    variant = parameter(
        [
            "homefs",
            "aifs",
            "userfs",
            "projectfs",
            "localfs",
            "modulepath",
            "numanodes",
            "ibvdev",
            "os",
            "kernel",
        ]
    )
    maintainers = ["rana.selim@kaust.edu.sa"]
    descr = "System sanity check on ibex nodes"
    tags = {"fs", "acceptance"}
    sourcesdir = None
    time_limit = "10m"


@rfm.simple_test
class system_cpu(system_check):
    """Define system checks variants for CPUs."""

    valid_systems = ["ibex:login", "ibex:batch"]
    valid_prog_environs = ["cpustack_builtin"]
    sourcesdir = None
    executable = "mount"
    time_limit = "10m"
    tags = {"system", "acceptance", "cpu", "fs", "sys", "singlenode"}

    @run_after("init")
    def setting_parameters(self):
        """Define test variants sanity and executables."""
        variant_map = {
            "homefs": ("mount", r"/home/home"),
            "aifs": ("mount", r"/ibex/ai"),
            "userfs": ("mount", r"/ibex/user"),
            "projectfs": ("mount", r"/ibex/project"),
            "localfs": ("mount", r"/local"),
            "modulepath": (
                "echo $MODULEPATH",
                (
                    r"/sw/rl9c/modulefiles/applications:"
                    r"/sw/rl9c/modulefiles/compilers:"
                    r"/sw/rl9c/modulefiles/libs:"
                    r"/sw/services_rl9/modulefiles"
                ),
            ),
            "numanodes": ("numactl -H", r"2 nodes"),
            "ibvdev": ("ibv_devinfo -l", r"mlx5_0"),
            "os": ("cat /etc/redhat-release", r"Rocky Linux release 9.4 \(Blue Onyx\)"),
            "kernel": ("uname -r ", r"5.14.0-427.20.1.el9_4.0.1.x86_64"),
        }

        cmd, pattern = variant_map[self.variant]
        self.executable = cmd
        self.sanity_patterns = sn.assert_found(pattern, self.stdout)


@rfm.simple_test
class system_gpu(system_check):
    """Define system checks variants for GPUs."""

    variant = parameter(
        [
            "homefs",
            "aifs",
            "userfs",
            "projectfs",
            "localfs",
            "modulepath",
            "numanodes",
            "ibvdev",
            "nvidiasmi",
            "devicequery",
            "os",
            "kernel",
            "peermemserivce",
            "modpeermem",
            "modgdrdrv",
        ]
    )

    descr = "System sanity check on gpu nodes"
    valid_systems = ["ibex:gpu", "ibex:gpu24", "ibex:gpu_wide24"]
    valid_prog_environs = ["gpustack_builtin"]
    num_gpus_per_node = 1
    num_tasks = 1
    sourcesdir = None
    executable = "mount"
    time_limit = "10m"
    tags = {"fs", "acceptance", "gpu", "system", "sys", "singlenode"}

    @run_after("init")
    def setting_parameters(self):
        """Define test variants sanity and executables."""
        variant_map = {
            "homefs": ("mount", r"/home/home"),
            "aifs": ("mount", r"/ibex/ai"),
            "userfs": ("mount", r"/ibex/user"),
            "projectfs": ("mount", r"/ibex/project"),
            "localfs": ("mount", r"/local"),
            "modulepath": (
                "echo $MODULEPATH",
                (
                    r"/sw/rl9g/modulefiles/libs:"
                    r"/sw/rl9g/modulefiles/compilers:"
                    r"/sw/rl9g/modulefiles/applications:"
                    r"/sw/services_rl9/modulefiles"
                ),
            ),
            "nvidiasmi": ("nvidia-smi", r"NVIDIA-SMI"),
            "numanodes": ("numactl -H", r" 2 nodes"),
            "ibvdev": ("ibv_devinfo -l", r"mlx5_0"),
            "devicequery": ("./deviceQuery", r"Result = PASS"),
            "os": ("cat /etc/redhat-release", r"Rocky Linux release 9.4 \(Blue Onyx\)"),
            "kernel": ("uname -r ", r"5.14.0-427.20.1.el9_4.0.1.x86_64"),
            "peermemserivce": (
                "systemctl status nv_peer_mem",
                r"Loaded:\s+loaded\s+\(/etc/rc\.d/init\.d/nv_peer_mem; generated\)",
            ),
            "modpeermem": ("lsmod | grep -o nv_peer_mem", r"nv_peer_mem"),
            "modgdrdrv": ("lsmod | grep -o gdrdrv", r"gdrdrv"),
        }

        cmd, pattern = variant_map[self.variant]
        self.executable = cmd
        if self.variant == "devicequery":
            self.sourcesdir = "../src/devicequery"
        self.sanity_patterns = sn.assert_found(pattern, self.stdout)

    @run_before("run")
    def set_job_options(self):
        """Define extra test resources."""
        self.job.options = ["--partition=batch", "--gpus=1", "--gpus-per-node=1"]
