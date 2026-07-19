import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class Cuda_device_checks(rfm.RegressionTest):
    """
    Define base class for CUDA device number check.
    """

    variant = parameter(
        ["v100_4", "v100_8", "p100", "rtx2080ti", "a100_4", "rtx4090_singlegpu", "h200_4", "h200_8"]
    )

    @run_after("init")
    def setting_variables(self):
        """
        Define test variants for GPUs.
        """
        self.descr = "CUDA Device query"
        self.constraint = self.variant
        self.tags = {
            "gpu",
            self.variant,
            "acceptance",
            "device_query",
            "cuda",
            "singlenode",
        }
        # Environment settings
        self.valid_systems = ["ibex:batch"]
        self.valid_prog_environs = ["gpustack_cuda"]
        self.sourcesdir = "../src/cuda/device_check"
        self.time_limit = "10m"
        if self.variant in ("v100_8", "rtx2080ti", 'h200_8'):
            self.num_gpus_per_node = 8
        elif self.variant == "rtx4090_singlegpu":
            self.num_gpus_per_node = 1
        else:
            self.num_gpus_per_node = 4

        # Resource and runtime settings
        self.num_tasks = 1

        # Build source using makefile provided in the resourcesdir
        self.build_system = "Make"
        # In the run phase invoke the executable name as below
        self.prerun_cmds = ["./env.sh"]
        self.executable = "./a.out"
        if self.variant in ("v100_4", "v100_8"):
            self.extra_resources = {"constraint": {"type": "v100"}}
        elif self.variant == "p100":
            self.extra_resources = {"constraint": {"type": "p100"}}
        elif self.variant == "rtx2080ti":
            self.extra_resources = {"constraint": {"type": "rtx2080ti"}}
        elif self.variant == "a100":
            self.extra_resources = {"constraint": {"type": "4gpus,a100"}}
        elif self.variant == "rtx4090_singlegpu":
            self.extra_resources = {"constraint": {"type": "gpu_rtx4090"}}
            self.tags.add("rtx4090")
            self.tags.discard("acceptance")
        elif self.variant in ("h200_4", "h200_8"):
            self.extra_resources = {"constraint": {"type": "h200"}}

        # Validation
        self.sanity_patterns = sn.assert_found(r"Devcount", self.stdout)
        # Performance check

        self.perf_patterns = {
            self.variant: sn.extractsingle(
                r"Devcount\s+(?P<devices>\S+)", self.stdout, "devices", int
            )
        }
        self.reference = {
            "ibex": {
                "p100": (4, None, None, "devices"),
                "v100_4": (4, None, None, "devices"),
                "v100_8": (8, None, None, "devices"),
                "rtx2080ti": (8, None, None, "devices"),
                "rtx4090_singlegpu": (1, None, None, "devices"),
                "a100_4": (4, None, None, "devices"),
                "h200_4": (4, None, None, "devices"),
                "h200_8": (8, None, None, "devices"),
            },
        }

        self.maintainers = ["mohsin.shaikh@kaust.edu.sa"]
