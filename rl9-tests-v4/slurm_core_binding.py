import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class slurm_core_binding(rfm.RunOnlyRegressionTest):
    @run_after('init')
    def setting_variables(self):
        self.descr = 'SLURM core binding test: verify SLURM_CPUS_PER_TASK'
        self.valid_systems = ['ibex:batch']
        self.valid_prog_environs = ['cpustack_builtin']
        self.sourcesdir = None
        self.num_tasks = 1
        self.num_cpus_per_task = 4
        self.time_limit = '10m'
        self.executable = 'printenv'
        self.executable_opts = ['SLURM_CPUS_PER_TASK']
        self.sanity_patterns = sn.or_(
            sn.assert_found(r'^4$', self.stdout),   
            sn.assert_found(r'^4$', self.stderr)    
        )
        self.sanity_patterns = sn.assert_found(r'4', self.stdout)
        self.maintainers = ['moamen.mohamed@kaust.edu.sa']
        self.tags = {'slurm', 'core_binding', 'cpu', 'singlenode'}
