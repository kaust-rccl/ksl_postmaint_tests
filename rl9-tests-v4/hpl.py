import reframe as rfm
import reframe.utility.sanity as sn


class hpl_test(rfm.RunOnlyRegressionTest):
    """
    Define base class for HPL test.
    """

    maintainers = ["mohamed.elgharawy@kaust.edu.sa"]
    descr = "running hpl tests for cpu/gpu"
    path = "HPL.out"


@rfm.simple_test
class hpl_cpu(hpl_test):
    """
    Define test variants for CPUs.
    """

    variant = parameter(["intel", "amd", "intel_xeon8568"])
    valid_systems = ["ibex:batch"]
    tags = {"hpl", "cpu", "singlenode", "acceptance"}
    reference = {
        "ibex": {
            "amd": (2600, -0.06, None, "Gflops"),
            "intel": (1800, -0.06, None, "Gflops"),
            "intel_xeon8568": (2200, -0.06, 0.01, "Gflops"),
        }
    }

    @run_after("init")
    def setting_variables(self):
        """
        Define test resources.
        """
        if self.variant == "intel":
            self.valid_systems = ["ibex:batch"]
            self.valid_prog_environs = ["cpustack_builtin"]
            self.time_limit = "10m"
            self.sourcesdir = "../src/hpl/cpu/intel"

            self.modules = ["openmpi/4.1.4/intel2022.3"]
            self.num_tasks = 1
            self.num_tasks_per_node = 1
            self.num_cpus_per_task = 40
            self.prerun_cmds = ["./env.sh"]
            self.executable = " srun -c ${SLURM_CPUS_PER_TASK} ./xhpl"
            self.extra_resources = {
                "constraint": {"type": "intel"},
                "nodes": {"num_of_nodes": "1"},
            }
            self.tags |= {"intel"}
        elif self.variant == "amd":
            self.valid_systems = ["ibex:batch"]
            self.valid_prog_environs = ["cpustack_builtin"]
            self.time_limit = "10m"
            self.sourcesdir = "../src/hpl/cpu/amd"
            self.modules = ["mpich/4.2.0/intel2022.3", "openmpi/4.1.4/gnu11.2.1"]
            self.num_tasks = 128
            self.num_tasks_per_node = 128
            self.num_cpus_per_task = 1
            self.prerun_cmds = ["./env.sh"]
            self.executable = "mpirun -np 128 -mca ucx -x ./xhpl"
            self.extra_resources = {
                "memory": {"size": "450G"},
                "constraint": {"type": "amd"},
                "nodes": {"num_of_nodes": "1"},
            }
            self.tags |= {"amd"}
        elif self.variant == "intel_xeon8568":
            self.valid_systems = ["ibex:batch"]
            self.valid_prog_environs = ["cpustack_builtin"]
            self.time_limit = "10m"
            self.sourcesdir = "../src/hpl/cpu/intel"

            self.modules = ["openmpi/4.1.4/intel2022.3"]
            self.num_tasks = 1
            self.num_tasks_per_node = 1
            self.num_cpus_per_task = 94
            self.num_gpus_per_node = 1 # Current configuration of H200 node requires to allocate a single GPU
            self.prerun_cmds = [
                "export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}",
                "export MKL_NUM_THREADS=${SLURM_CPUS_PER_TASK}",
                "export OMP_PROC_BIND=close",
                "export OMP_PLACES=cores",
                "./env.sh",
            ]
            self.executable = (
                "srun --cpus-per-task=${SLURM_CPUS_PER_TASK} " \
                "--cpu-bind=none " \
                "./xhpl"
            )
            self.extra_resources = {
                "constraint": {"type": "intel"},
                "nodes": {"num_of_nodes": "1"},
            }
            self.tags |= {"intel"}

    @run_before("sanity")
    def set_sanity_patterns(self):
        """
        Define test sanity pattern to check test is able to run.
        """
        self.sanity_patterns = sn.all(
            [
                sn.assert_found("End of Tests.", self.stdout),
                sn.assert_found(
                    "0 tests completed and failed residual checks", self.stdout
                ),
                sn.assert_found(
                    "0 tests skipped because of illegal input values.", self.stdout
                ),
            ]
        )

    @run_before("performance")
    def set_perf_patterns(self):
        """
        Define test performance pattern.
        Used to capture performance number from output file.
        """
        self.perf_patterns = {
            self.variant: sn.extractsingle(
                r"^W[R|C]\S+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d[\d.]+\s+(?P<Gflops>\d[\d.eE+]+)",
                self.stdout,
                "Gflops",
                float,
            )
        }


@rfm.simple_test
class hpl_gpu(hpl_test):
    """
    Define test variants for GPUs.
    """

    variant = parameter(
        ["p100", "v100_4", "v100_8", "a100_4", "a100_8", "rtx4090_singlegpu", "h200_8"]
    )
    valid_systems = ["ibex:batch"]
    valid_prog_environs = ["gpustack_builtin"]
    tags = {"hpl", "gpu", "singlenode", "acceptance"}
    sourcesdir = "../src/hpl/gpu"
    time_limit = "10m"

    reference = {
        "ibex": {
            "p100": (1350, -0.05, None, "Gflops"),
            "v100_8": (35600, -0.05, None, "Gflops"),
            "v100_4": (16500, -0.05, None, "Gflops"),
            "a100_4": (56000, -0.05, None, "Gflops"),
            "a100_8": (92500, -0.05, None, "Gflops"),
            "rtx4090_singlegpu": (1220, -0.05, None, "Gflops"),
            "h200_8": (300100, -0.05, None, "Gflops"),
        }
    }

    @run_after("init")
    def setting_variables(self):
        """
        Define test resources.
        """
        if self.variant == "p100":
            self.num_tasks = 4
            self.executable = (
                "srun -u -n ${SLURM_NTASKS} -c ${SLURM_CPUS_PER_TASK} "
                "--cpu-bind=none singularity run --nv $IMAGE hpl.sh "
                "--cpu-affinity 0,3-7:8-13:20-25:26-31  "
                "--cpu-cores-per-rank ${CPUS} "
                "--gpu-affinity 0:1:2:3 --dat ./HPL.dat.p100"
            )
            self.num_cpus_per_task = 8
            self.num_gpus_per_node = 4
            self.extra_resources = {
                "memory": {"size": "230G"},
                "constraint": {"type": "p100"},
            }

            self.prerun_cmds = [
                "module purge",
                "module load rl9-gpustack",
                "module load singularity",
                "export IMAGE=./hpl_sing.sif",
                "export CPUS=6",
                "export HPL=./HPL.out",
                "echo hostname > HPL.out",
                "./env.sh",
            ]
            self.tags |= {"p100"}

        elif self.variant == "rtx4090_singlegpu":
            self.num_tasks = 1
            self.executable = (
                "srun -u -n ${SLURM_NTASKS} -c ${SLURM_CPUS_PER_TASK} "
                "--cpu-bind=none singularity run --nv $IMAGE hpl.sh "
                "--cpu-affinity 0,3-7  --cpu-cores-per-rank ${CPUS} "
                "--gpu-affinity 0 --dat ./HPL.dat.4090"
            )
            self.num_cpus_per_task = 8
            self.num_gpus_per_node = 1
            self.extra_resources = {
                "memory": {"size": "220G"},
                "constraint": {"type": "gpu_rtx4090"},
            }

            self.prerun_cmds = [
                "module purge",
                "module load rl9-gpustack",
                "module load singularity",
                "export IMAGE=./hpl_sing.sif",
                "export CPUS=6",
                "export HPL=./HPL.out",
                "echo hostname > HPL.out",
                "./env.sh",
            ]
            self.tags |= {"rtx4090"}
            self.tags.discard("acceptance")

        elif self.variant == "v100_8":
            self.num_tasks = 8
            self.executable = (
                "srun -u -n ${SLURM_NTASKS} -c ${SLURM_CPUS_PER_TASK} "
                "--cpu-bind=none singularity run --nv $IMAGE hpl.sh "
                "--cpu-affinity 0,3-5:7-10:12-15:17-20:24-27:28-31:32-35:36-39   "
                "--cpu-cores-per-rank ${CPUS} --gpu-affinity 0:1:2:3:4:5:6:7  "
                "--dat ./HPL.dat.v100.G8N1"
            )
            self.num_cpus_per_task = 5
            self.extra_resources = {
                "memory": {"size": "450G"},
                "constraint": {"type": "v100,gpu_ai"},
            }

            self.prerun_cmds = [
                "module purge",
                "module load rl9-gpustack",
                "module load singularity",
                "export IMAGE=./hpl_sing.sif",
                "export CPUS=5",
                "export HPL=./HPL.out",
                "echo hostname > HPL.out",
                "./env.sh",
            ]
            self.tags |= {"v100_8"}

        elif self.variant == "v100_4":
            self.num_tasks = 4
            self.num_cpus_per_task = 7
            self.num_gpus_per_node = 4
            self.extra_resources = {
                "memory": {"size": "340G"},
                "constraint": {"type": "v100,cpu_intel_gold_6142"},
            }
            self.executable = (
                "srun -u -n ${SLURM_NTASKS} -c ${SLURM_CPUS_PER_TASK} "
                "--cpu-bind=none singularity run --nv $IMAGE hpl.sh "
                "--cpu-affinity 0,3-5:7-10:18-21:23-26 --cpu-cores-per-rank ${CPUS} "
                "--gpu-affinity 0:1:2:3 --dat ./HPL.dat.v100.G4N1"
            )
            self.prerun_cmds = [
                "module purge",
                "module load rl9-gpustack",
                "module load singularity",
                "export IMAGE=./hpl_sing.sif",
                "export CPUS=4",
                "export HPL=./HPL.out",
                "echo hostname > HPL.out",
                "./env.sh",
            ]
            self.tags |= {"v100_4"}

        elif self.variant == "a100_8":
            self.num_tasks = 8
            self.num_gpus_per_node = 8
            self.extra_resources = {
                "memory": {"size": "850G"},
                "constraint": {"type": "a100,8gpus"},
                "nodes": {"num_of_nodes": "1"},
            }
            self.executable = (
                "srun -u -n ${SLURM_NTASKS} -c ${SLURM_CPUS_PER_TASK} "
                "--cpu-bind=none singularity run --nv $IMAGE hpl.sh "
                "--cpu-affinity 30-36:45-51:0,3-7:16-22:90-96:105-111:64-70:75-81 "
                "--cpu-cores-per-rank ${CPUS} --gpu-affinity 0:1:2:3:4:5:6:7 "
                "--dat ./HPL.dat.a100.G8N1"
            )
            self.num_cpus_per_task = 15

            self.prerun_cmds = [
                "module purge",
                "module load rl9-gpustack",
                "module load singularity",
                "export IMAGE=./hpl_sing.sif",
                "export CPUS=7",
                "export OMPI_MCA_btl_openib_warn_no_device_params_found=0",
                "./env.sh",
            ]
            self.tags |= {"a100_8"}

        elif self.variant == "a100_4":
            self.num_tasks = 4
            self.num_gpus_per_node = 4
            self.extra_resources = {
                "memory": {"size": "450G"},
                "constraint": {"type": "a100,4gpus"},
                "nodes": {"num_of_nodes": "1"},
            }
            self.executable = (
                "srun -u -n ${SLURM_NTASKS} -c ${SLURM_CPUS_PER_TASK} "
                "--cpu-bind=sockets,verbose singularity run --nv $IMAGE hpl.sh "
                "--cpu-cores-per-rank ${CPUS} "
                "--cpu-affinity 0,3-7:16-22:38-44:52-59 "
                "--gpu-affinity 2:3:0:1  --dat ./HPL.dat.a100.G4N1"
            )
            self.num_cpus_per_task = 15
            self.tags |= {"a100_4"}

            self.prerun_cmds = [
                "module purge",
                "module load rl9-gpustack",
                "module load singularity",
                "export IMAGE=./hpl_sing.sif",
                "export CPUS=7",
                "export OMPI_MCA_btl_openib_warn_no_device_params_found=0",
                "./env.sh",
            ]

        elif self.variant == "h200_8":
            self.num_tasks = 1
            self.num_gpus_per_node = 8
            self.num_cpus_per_task = 94
            
            self.extra_resources = {
                "memory": {"size": "850G"},
                "constraint": {"type": "h200,8gpus"},
                "nodes": {"num_of_nodes": "1"},
            }

            self.executable = (
                "singularity run --nv "
                "-B .:/my-dat-files "
                "$IMAGE "
                "mpirun --oversubscribe --bind-to none -np 8 "
                "/workspace/hpl.sh "
                "--dat /my-dat-files/HPL.dat.h200.G8N1 "
                "--cpu-affinity "
                "0,3-9:10-16:17-23:24-47:48-55:56-63:64-71:72-95 "
                "--mem-affinity "
                "0:0:0:1:2:2:2:3 "
                "--gpu-affinity "
                "0:1:2:3:4:5:6:7 "
            )

            self.prerun_cmds = [
                "module purge",
                "module load rl9-gpustack",
                "module load singularity",
                "export IMAGE=./hpl_sing_h200.sif",
                "export OMPI_MCA_hwloc_base_binding_policy=none",
            ]

            self.tags |= {"h200_8"}
            
    @run_before("run")
    def set_job_options(self):
        """
        Define job options.
        """
        if self.variant in ("v100_8", "a100_8"):
            self.job.options = ["--partition=batch", "--gpus=8", "--gpus-per-node=8"]
        elif self.variant in ("a100_4", "v100_4", "p100"):
            self.job.options = ["--partition=batch"]

    @run_before("sanity")
    def set_sanity_patterns(self):
        """
        Define test sanity pattern to check test is able to run.
        """
        self.sanity_patterns = sn.all(
            [
                sn.assert_found("End of Tests.", self.path),
                sn.assert_found(
                    "0 tests completed and failed residual checks", self.path
                ),
                sn.assert_found(
                    "0 tests skipped because of illegal input values.", self.path
                ),
            ]
        )

    @run_before("performance")
    def set_perf_patterns(self):
        """
        Define test performance pattern.
        Used to capture performance number from output file.
        """
        self.perf_patterns = {
            self.variant: sn.extractsingle(
                r"^W[R|C]\S+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d[\d.]+\s+(?P<Gflops>\d[\d.eE+]+)",
                self.path,
                "Gflops",
                float,
            )
        }
