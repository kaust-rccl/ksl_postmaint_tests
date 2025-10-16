import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class nccl_tests(rfm.RunOnlyRegressionTest):
    """Define base class for nccl test."""

    variant = parameter(
        [
            "v100_8_singlenode",
            "v100_4_singlenode",
            "v100_8_multinode",
            "a100_4_singlenode",
            "a100_4_multinode",
            "a100_8_singlenode",
            "a100_8_multinode",
        ]
    )

    ## TEST BASIC INFO
    maintainers = ["rana.selim@kaust.edu.sa"]
    descr = "running nccl tests"

    ## SETTING TEST ENV
    sourcesdir = "../src/env"
    valid_prog_environs = ["gpustack_builtin"]
    valid_systems = ["ibex:batch"]
    modules = ["openmpi/4.1.4/gnu11.2.1-cuda11.8", "cuda/11.8", "nccl/2.17.1-cuda11.8"]
    reference = {
        "ibex": {
            "v100_8_singlenode": (100, -0.1, None, "GB/s"),
            "v100_4_singlenode": (100, -0.1, None, "GB/s"),
            "a100_4_singlenode": (230, -0.1, None, "GB/s"),
            "a100_8_singlenode": (230, -0.1, None, "GB/s"),
            "v100_8_multinode": (100, -0.1, None, "GB/s"),
            "a100_4_multinode": (40, -0.1, None, "GB/s"),
            "a100_8_multinode": (100.0, -0.1, None, "GB/s"),
        }
    }

    @run_after("init")
    def setting_variables(self):
        """Define test resources per variant."""

        common_exec = (
            "srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} "
            "-c ${SLURM_CPUS_PER_TASK} all_reduce_perf "
            "-b 4G -e 4G -f 2 -g 1 -c 0 -n 50 -w 20"
        )

        variant_map = {
            "v100_4_singlenode": {
                "tags": {"singlenode"},
                "time_limit": "30m",
                "num_tasks": 4,
                "num_tasks_per_node": 4,
                "num_cpus_per_task": 7,
                "num_gpus_per_node": 4,
                "prerun_cmds": ["./env.sh"],
                "extra_resources": {
                    "memory": {"size": "300G"},
                    "constraint": {"type": "v100,cpu_intel_gold_6142"},
                },
                "executable": common_exec,
            },
            "v100_8_singlenode": {
                "tags": {"singlenode"},
                "time_limit": "30m",
                "num_tasks": 8,
                "num_tasks_per_node": 8,
                "num_cpus_per_task": 5,
                "num_gpus_per_node": 8,
                "prerun_cmds": ["./env.sh"],
                "extra_resources": {
                    "memory": {"size": "700G"},
                    "constraint": {"type": "v100"},
                },
                "executable": common_exec,
            },
            "a100_8_singlenode": {
                "tags": {"singlenode"},
                "time_limit": "30m",
                "num_tasks": 8,
                "num_tasks_per_node": 8,
                "num_cpus_per_task": 15,
                "num_gpus_per_node": 8,
                "prerun_cmds": ["./env.sh"],
                "extra_resources": {"constraint": {"type": "a100"}},
                "executable": common_exec,
            },
            "v100_8_multinode": {
                "time_limit": "30m",
                "num_tasks": 16,
                "num_tasks_per_node": 8,
                "num_cpus_per_task": 5,
                "extra_resources": {"constraint": {"type": "v100,gpu_ai"}},
                "executable": (
                    "srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} "
                    "-c ${SLURM_CPUS_PER_TASK} "
                    "--cpu-bind=map_cpu:0,6,11,19,24,29,33,38 "
                    "all_reduce_perf -b 4G -e 4G -f 2 -g 1 -c 0 -n 50 -w 20"
                ),
                "prerun_cmds": [
                    "./env.sh",
                    "export NCCL_DEBUG=INFO",
                    "export NCCL_ALGO=Tree",
                    "export NCCL_NET_GDR_LEVEL=4",
                    "export NCCL_IB_HCA=mlx5",
                    "echo ${SLURM_NODELIST}",
                    "module list",
                ],
            },
            "a100_4_singlenode": {
                "tags": {"singlenode"},
                "time_limit": "30m",
                "num_tasks": 4,
                "num_tasks_per_node": 4,
                "num_cpus_per_task": 15,
                "num_gpus_per_node": 4,
                "prerun_cmds": ["./env.sh"],
                "extra_resources": {"constraint": {"type": "a100,4gpus"}},
                "executable": common_exec,
            },
            "a100_4_multinode": {
                "time_limit": "30m",
                "num_tasks": 8,
                "num_tasks_per_node": 4,
                "num_cpus_per_task": 15,
                "extra_resources": {"constraint": {"type": "a100,4gpus"}},
                "executable": (
                    "srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} "
                    "-c ${SLURM_CPUS_PER_TASK} "
                    "--cpu-bind=map_cpu:35,45,4,25 all_reduce_perf "
                    "-b 4G -e 4G -f 2 -g 1 -c 0 -n 50 -w 20"
                ),
                "prerun_cmds": [
                    "export NCCL_DEBUG=INFO",
                    "echo ${SLURM_NODELIST}",
                    "module list",
                    "export NCCL_ALGO=Tree",
                    "export NCCL_NET_GDR_LEVEL=4",
                    "export NCCL_IB_HCA=mlx5",
                ],
            },
            "a100_8_multinode": {
                "time_limit": "30m",
                "num_tasks": 16,
                "num_tasks_per_node": 8,
                "num_cpus_per_task": 15,
                "extra_resources": {"constraint": {"type": "a100,8gpus"}},
                "executable": (
                    "srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} "
                    "-c ${SLURM_CPUS_PER_TASK} "
                    "--cpu-bind=map_cpu:35,45,4,25,105,115,75,85 all_reduce_perf "
                    "-b 4G -e 4G -f 2 -g 1 -c 0 -n 50 -w 20"
                ),
                "prerun_cmds": [
                    "export NCCL_DEBUG=INFO",
                    "export NCCL_ALGO=Tree",
                    "export NCCL_NET_GDR_LEVEL=4",
                    "export NCCL_IB_HCA=mlx5",
                    "echo ${SLURM_NODELIST}",
                    "module list",
                ],
            },
        }

        cfg = variant_map[self.variant]
        self.tags = (
            getattr(self, "tags", set())
            | {"gpu", self.variant, "acceptance", "nccl"}
            | cfg.get("tags", set())
        )
        for key, val in cfg.items():
            if key != "tags":
                setattr(self, key, val)

    @run_before("run")
    def set_job_options(self):
        """Define extra resources per variant."""
        job_opts = {
            "v100_8_multinode": ["--gpus=16", "--gpus-per-node=8"],
            "a100_4_multinode": ["--gpus=8", "--gpus-per-node=4"],
            "a100_8_multinode": ["--nodes=2", "--gpus=16", "--gpus-per-node=8"],
        }
        if self.variant in job_opts:
            self.job.options = job_opts[self.variant]

    @run_before("sanity")
    def set_sanity_patterns(self):
        """Define test sanity pattern to check test is able to run."""
        self.sanity_patterns = sn.assert_found(r"# Avg bus bandwidth", self.stdout)

    @run_before("performance")
    def set_perf_patterns(self):
        """Define test performance pattern to capture performance number."""
        self.perf_patterns = {
            self.variant: sn.extractsingle(
                r"^#\s[A]\w+\s\w+\s\w+\s+[:]\s(?P<Busbw>\d*\.\d+)",
                self.stdout,
                "Busbw",
                float,
            )
        }
