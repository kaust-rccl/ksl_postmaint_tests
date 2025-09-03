import os
import reframe as rfm
import reframe.utility.sanity as sn


class Amber_test(rfm.RunOnlyRegressionTest):
    maintainers = ["ahmed.khatab@kaust.edu.sa"]
    descr = "Run Amber checks"
    valid_systems = ["ibex:batch"]
    valid_prog_environs = ["gpustack_builtin"]
    sourcesdir = "../src/amber"
    modules = ["amber/24/openmpi4.1.4_cuda12.1"]
    time_limit = "10m"


@rfm.simple_test
class amber_a100(Amber_test):
    variant = parameter(["a100_1", "a100_2", "a100_4"])

    @run_after("init")
    def setting_variables(self):
        self.tags = {"gpu", "acceptance", "amber", "a100", self.variant}
        if self.variant == "a100_1":
            self.num_tasks = 1
            self.num_tasks_per_node = 1

            self.executable = "pmemd.cuda"
            self.executable_opts = [
                "-O",
                "-i mdin.GPU",
                "-o mdout",
                "-p JAC.prmtop",
                "-c JAC.inpcrd",
                "-r restrt",
                "-x mdcrd",
            ]
            self.reference = {
                "ibex:batch": {"Elapsed_time": (1050.00, -0.05, None, "ns/day")}
            }

        elif self.variant == "a100_2":
            self.num_tasks = 2
            self.num_tasks_per_node = 2

            self.executable = "mpirun -np 2 pmemd.cuda.MPI"
            self.executable_opts = [
                "-O",
                "-i mdin.GPU",
                "-o mdout",
                "-p JAC.prmtop",
                "-c JAC.inpcrd",
                "-r restrt",
                "-x mdcrd",
            ]
            self.reference = {
                "ibex:batch": {"Elapsed_time": (1250.00, -0.05, None, "ns/day")}
            }

        elif self.variant == "a100_4":
            self.num_tasks = 4
            self.num_tasks_per_node = 4

            self.executable = "mpirun -np 4 pmemd.cuda.MPI"
            self.executable_opts = [
                "-O",
                "-i mdin.GPU",
                "-o mdout",
                "-p JAC.prmtop",
                "-c JAC.inpcrd",
                "-r restrt",
                "-x mdcrd",
            ]
            self.reference = {
                "ibex:batch": {"Elapsed_time": (1300.00, -0.05, None, "ns/day")}
            }

        self.sanity_patterns = sn.assert_found(r"ns/day =", "mdout")

        # Extract the second ns/day using a regex
        self.perf_patterns = {
            "Elapsed_time": sn.extractsingle(
                r"ns/day\s*=\s*(\d+\.\d+)", "mdout", 1, float
            )
        }

    @run_before("run")
    def set_job_options(self):
        if self.variant == "a100_1":
            self.job.options = [
                "--constraint=a100",
                "--gpus=1",
                "--cpus-per-task=4",
                "--mem=50G",
            ]
        elif self.variant == "a100_2":
            self.job.options = [
                "--constraint=a100",
                "--nodes=1",
                "--gpus=2",
                "--cpus-per-task=4",
                "--mem=50G",
            ]
        elif self.variant == "a100_4":
            self.job.options = [
                "--constraint=a100",
                "--nodes=1",
                "--gpus=4",
                "--cpus-per-task=4",
                "--mem=50G",
            ]


@rfm.simple_test
class amber_v100(Amber_test):
    variant = parameter(["v100_1", "v100_2", "v100_4"])

    @run_after("init")
    def setting_variables(self):
        self.tags = {"gpu", "acceptance", "amber", "v100", self.variant}
        if self.variant == "v100_1":
            self.num_tasks = 1
            self.num_tasks_per_node = 1

            self.executable = "pmemd.cuda"
            self.executable_opts = [
                "-O",
                "-i mdin.GPU",
                "-o mdout",
                "-p JAC.prmtop",
                "-c JAC.inpcrd",
                "-r restrt",
                "-x mdcrd",
            ]
            self.reference = {
                "ibex:batch": {"Elapsed_time": (900.00, -0.05, None, "ns/day")}
            }

        elif self.variant == "v100_2":
            self.num_tasks = 2
            self.num_tasks_per_node = 2

            self.executable = "mpirun -np 2 pmemd.cuda.MPI"
            self.executable_opts = [
                "-O",
                "-i mdin.GPU",
                "-o mdout",
                "-p JAC.prmtop",
                "-c JAC.inpcrd",
                "-r restrt",
                "-x mdcrd",
            ]
            self.reference = {
                "ibex:batch": {"Elapsed_time": (1100.00, -0.05, None, "ns/day")}
            }

        elif self.variant == "v100_4":
            self.num_tasks = 4
            self.num_tasks_per_node = 4
            # self.num_tasks_per_node = 2

            self.executable = "mpirun -np 4 pmemd.cuda.MPI"
            self.executable_opts = [
                "-O",
                "-i mdin.GPU",
                "-o mdout",
                "-p JAC.prmtop",
                "-c JAC.inpcrd",
                "-r restrt",
                "-x mdcrd",
            ]
            self.reference = {
                "ibex:batch": {"Elapsed_time": (1000.00, -0.05, None, "ns/day")}
            }

        self.sanity_patterns = sn.assert_found(r"ns/day =", "mdout")

        # Extract the second ns/day using a regex
        self.perf_patterns = {
            "Elapsed_time": sn.extractsingle(
                r"ns/day\s*=\s*(\d+\.\d+)", "mdout", 1, float
            )
        }

    @run_before("run")
    def set_job_options(self):
        if self.variant == "v100_1":
            self.job.options = [
                "--constraint=v100",
                "--gpus=1",
                "--cpus-per-task=4",
                "--mem=50G",
            ]
        elif self.variant == "v100_2":
            self.job.options = [
                "--constraint=v100",
                "--nodes=1",
                "--gpus=2",
                "--cpus-per-task=4",
                "--mem=50G",
            ]
        elif self.variant == "v100_4":
            self.job.options = [
                "--constraint=v100",
                "--nodes=1",
                "--gpus=4",
                "--cpus-per-task=4",
                "--mem=50G",
            ]


@rfm.simple_test
class amber_cpu(Amber_test):
    variant = parameter(["cpu"])

    @run_after("init")
    def setting_variables(self):
        self.tags = {"gpu", "acceptance", "amber", self.variant}
        self.num_tasks = 64
        self.prerun_cmds = ["export OMP_NUM_THREADS=64"]
        self.executable = "mpirun -np 64 pmemd.MPI"
        self.executable_opts = [
            "-O",
            "-i mdin.CPU",
            "-o mdout",
            "-p JAC.prmtop",
            "-c JAC.inpcrd",
            "-r restrt",
            "-x mdcrd",
        ]
        self.reference = {
            "ibex:batch": {"Elapsed_time": (100.00, -0.1, None, "ns/day")}
        }

        self.sanity_patterns = sn.assert_found(r"ns/day =", "mdout")

        # Extract the second ns/day using a regex
        self.perf_patterns = {
            "Elapsed_time": sn.extractsingle(
                r"ns/day\s*=\s*(\d+\.\d+)", "mdout", 1, float
            )
        }

    @run_before("run")
    def set_job_options(self):
        if self.variant == "cpu":
            self.job.options = [
                "--constraint=a100",
                "--nodes=1",
                "--gpus=1",
                "--mem=50G",
            ]
