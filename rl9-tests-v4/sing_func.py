import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class sing_build(rfm.RunOnlyRegressionTest):
    """
    Define base class for singularity functionality tests.
    """

    @run_after("init")
    def setting_variables(self):
        """
        Define test information and resources.
        """
        self.maintainers = ["moamen.mohamed@kaust.edu.sa"]
        self.tags = {"sing_build", "sing_func", "cpu", "singularity", "singlenode"}
        self.valid_systems = ["ibex:batch"]
        self.valid_prog_environs = ["cpustack_gnu"]
        self.sourcesdir = "../src/singularity/func"
        self.time_limit = "10m"
        self.sanity_patterns = sn.assert_found(r"Build complete", self.stderr)
        self.descr = "Singularity Build a basic Definition File"
        self.modules = ["singularity/3.9.7"]
        self.num_tasks = 4
        self.num_tasks_per_node = 4
        self.executable = "singularity build --fakeroot sing.sif sing.def"


@rfm.simple_test
class sing_pull(rfm.RunOnlyRegressionTest):
    """
    Define test for singularity pull functionality.
    """

    @run_after("init")
    def setting_variables(self):
        """
        Define test resources.
        """
        self.maintainers = ["moamen.mohamed@kaust.edu.sa"]
        self.tags = {"sing_pull", "sing_func", "cpu", "singularity"}
        self.valid_systems = ["ibex:batch"]
        self.valid_prog_environs = ["cpustack_gnu"]
        self.time_limit = "10m"
        self.sanity_patterns = sn.assert_found(r"Creating SIF", self.stderr)
        self.descr = "Building a singularity image from a Dockerhub image"
        self.modules = ["singularity/3.9.7"]
        self.num_tasks = 4
        self.num_tasks_per_node = 4
        self.prerun_cmds = ["export SINGULARITY_DISABLE_CACHE=1"]
        self.executable = "singularity pull docker://python"


@rfm.simple_test
class sing_exec(rfm.RunOnlyRegressionTest):
    """
    Define test for singularity ecec functionality.
    """

    @run_after("init")
    def setting_variables(self):
        """
        Define test resources.
        """
        self.maintainers = ["moamen.mohamed@kaust.edu.sa"]
        self.tags = {"sing_exec", "sing_func", "cpu", "singularity"}
        self.valid_systems = ["ibex:batch"]
        self.valid_prog_environs = ["cpustack_gnu"]
        self.time_limit = "10m"
        self.sanity_patterns = sn.assert_found(r"Testing singularity exec", self.stdout)
        self.descr = "Running commands within singularity container"
        self.modules = ["singularity/3.9.7"]
        self.num_tasks = 4
        self.num_tasks_per_node = 4
        self.executable = (
            "singularity exec "
            "--fakeroot "
            "docker://ubuntu "
            'echo "Testing singularity exec"'
        )


@rfm.simple_test
class sing_entrypoint(rfm.RunOnlyRegressionTest):
    """
    Define test for singularity run functionality.
    """

    @run_after("init")
    def setting_variables(self):
        """
        Define test resources.
        """
        self.maintainers = ["moamen.mohamed@kaust.edu.sa"]
        self.tags = {"sing_entrypoint", "sing_func", "cpu", "singularity"}
        self.valid_systems = ["ibex:batch"]
        self.valid_prog_environs = ["cpustack_gnu"]
        self.sourcesdir = "../src/singularity/func"
        self.time_limit = "10m"
        self.sanity_patterns = sn.assert_found(r"Usage: genomad", self.stdout)
        self.descr = "Singularity run a container from an entrypoint"
        self.modules = ["singularity/3.9.7"]
        self.num_tasks = 4
        self.num_tasks_per_node = 4
        self.executable = "singularity run ./entrypoint.sif genomad -h"
