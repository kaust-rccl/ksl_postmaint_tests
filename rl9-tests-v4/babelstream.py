import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class babelstream_tests(rfm.RunOnlyRegressionTest):
    """
    Define base class for babelstream test.
    """

    variant = parameter(["a100_4_singlenode", "rtx4090_singlegpu", "h200_4_singlenode", "h200_8_singlenode"])

    ## TEST BASIC INFO
    maintainers = ["mohamed.elgharawy@kaust.edu.sa"]
    descr = "running babelstream tests on gpu nodes "
    ## SETTING TEST ENV
    sourcesdir = None
    valid_prog_environs = ["gpustack_builtin"]
    valid_systems = ["ibex:batch"]
    modules = ["gcc/12.2.0", "cuda/11.8"]
    reference = {
        "ibex": {
            "a100_4_singlenode": (7100000, -0.05, None, "MB/s"),
            "rtx4090_singlegpu": (3300000, -0.05, None, "MB/s"),
            "h200_4_singlenode": (17520257, -0.05, None, "MB/s"),
            "h200_8_singlenode": (35040514, -0.05, None, "MB/s"),
        }
    }

    ## RUN AND VALIDATE
    @run_after("init")
    def setting_variables(self):
        """
        Define test variants for GPUs.
        """
        self.time_limit = "20m"
        self.prerun_cmds = ["./env.sh"]
        self.executable = "srun ./run_script_ksl_cs_storm.sh"
        self.sourcesdir = "../src/babelstream"
        self.tags = {"babelstream", "gpu", self.variant, "acceptance", "singlenode"}

        if self.variant == "a100_4_singlenode":
            self.extra_resources = {
                "memory": {"size": "400G"},
                "constraint": {"type": "a100"},
                "nodes": {"num_of_nodes": "1"},
            }
            self.num_gpus_per_node = 4
            self.num_cpus_per_task = 56
            self.executable = "srun ./run_script_ksl_cs_storm.sh"
        elif self.variant == "rtx4090_singlegpu":
            self.extra_resources = {
                "memory": {"size": "220G"},
                "constraint": {"type": "gpu_rtx4090"},
            }
            self.num_gpus_per_node = 1
            self.num_cpus_per_task = 26
            self.executable = "srun ./run_script_ksl_cs_storm_4090.sh"
            self.tags.add("rtx4090")
            self.tags.discard("acceptance")
        elif self.variant == "h200_4_singlenode":
            self.extra_resources = {
                "memory": {"size": "400G"},
                "constraint": {"type": "h200"},
                "nodes": {"num_of_nodes": "1"},
            }
            self.num_gpus_per_node = 4
            self.num_cpus_per_task = 56
            self.executable = "srun ./run_script_ksl_cs_storm_h200_4gpu.sh"
        elif self.variant == "h200_8_singlenode":
            self.extra_resources = {
                "memory": {"size": "400G"},
                "constraint": {"type": "h200"},
                "nodes": {"num_of_nodes": "1"},
            }
            self.num_gpus_per_node = 8
            self.num_cpus_per_task = 56
            self.executable = "srun ./run_script_ksl_cs_storm_h200_8gpu.sh"

    @run_before("sanity")
    def set_sanity_patterns(self):
        """
        Define test sanity pattern to check test is able to run.
        """
        self.sanity_patterns = sn.assert_found(r"Triad\(node\)", self.stdout)

    @run_before("performance")
    def set_perf_patterns(self):
        """
        Define test performance pattern.
        Used to capture performance number from output file.
        """
        self.perf_patterns = {
            self.variant: sn.extractsingle(
                r"Triad\(node\)\s+(?P<Triad>\d*\.\d+)", self.stdout, "Triad", float
            )
        }
