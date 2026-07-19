import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class Cuda_power_checks(rfm.RunOnlyRegressionTest):
    """
    Define base class for GPU power limit test.
    """

    variant = parameter(["v100_4", "v100_8", "p100", "rtx2080ti", "a100_4", "a100_8", "h200_4", "h200_8"])

    @run_after("init")
    def setting_variables(self):
        """
        Define test variants for GPUs.
        """
        self.descr = "CUDA Power query"
        self.constraint = self.variant
        self.tags = {
            "gpu",
            self.variant,
            "acceptance",
            "power_query",
            "cuda",
            "singlenode",
        }
        # Environment settings
        self.valid_systems = ["ibex:batch"]

        self.valid_prog_environs = ["gpustack_cuda"]
        self.time_limit = "10m"
        if self.variant in ("v100_8", "rtx2080ti", "a100_8", "h200_8"):
            self.num_gpus_per_node = 8
        else:
            self.num_gpus_per_node = 4

        # Resource and runtime settings
        self.num_tasks = 1

        # In the run phase invoke the executable name as below
        self.prerun_cmds = ["./env.sh"]
        self.executable = (
            "bash -c 'nvidia-smi -q -d POWER "
            '| grep -i "Current Power Limit" '
            '| grep -v "N/A"\''
        )
        if self.variant in ("v100_4", "v100_8"):
            self.extra_resources = {"constraint": {"type": "v100"}}
        elif self.variant == "p100":
            self.extra_resources = {"constraint": {"type": "p100"}}
        elif self.variant == "rtx2080ti":
            self.extra_resources = {"constraint": {"type": "rtx2080ti"}}
        elif self.variant == "a100_4":
            self.extra_resources = {"constraint": {"type": "4gpus,a100"}}
        elif self.variant == "a100_8":
            self.extra_resources = {"constraint": {"type": "a100"}}
        elif self.variant in ("h200_4", "h200_8"):
            self.extra_resources = {"constraint": {"type": "h200"}}
        # Validation
        self.sanity_patterns = sn.assert_found(r"Current Power Limit", self.stdout)
        # Performance check
        power_limits = sn.extractall(
            r"Current Power Limit\s+:\s+(?P<watts>\d+\.\d+)\sW",
            self.stdout,
            "watts",
            float,
        )
        min_power = sn.min(power_limits)
        self.perf_patterns = {self.variant: min_power}
        self.reference = {
            "ibex": {
                "p100": (250.0, None, None, "watts"),
                "v100_4": (300.0, None, None, "watts"),
                "v100_8": (300.0, None, None, "watts"),
                "rtx2080ti": (250.0, None, None, "watts"),
                "a100_8": (400.0, None, None, "watts"),
                "a100_4": (400.0, None, None, "watts"),
                "h200_4": (700.0, None, None, "watts"),
                "h200_8": (700.0, None, None, "watts"),
            },
        }

        self.maintainers = ["mohamed.elgharawy@kaust.edu.sa"]
