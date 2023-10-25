import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.simple_test
class slurm_check(rfm.RunOnlyRegressionTest):
      variant= parameter(['slurmctld', 'squeue','sacct'])
      @run_after('init')
      def setting_variables(self):
        self.descr = 'SLURM check on ilogin and compute nodes'
        self.valid_systems = ['ibex:login','ibex:batch']
        self.valid_prog_environs = ['cpustack_builtin']
        self.sourcesdir=None
        self.num_tasks=1
        self.time_limit = '3m'
        if self.variant == "slurmctld":
            self.executable='scontrol ping'
            self.sanity_patterns =sn.assert_found(r'slurm-02 is UP',self.stdout)
        elif self.variant == "squeue":
            self.executable='squeue -u ismailiy'	
            self.sanity_patterns =sn.assert_found(r'NODELIST',self.stdout)
        elif self.variant == "sacct":
            self.executable='sacct'
            self.sanity_patterns =sn.assert_found(r'JobID           JobName  Partition    Account  AllocCPUS      State ExitCode ',self.stdout)

        self.maintainers = ['mohsin.shaikh@kaust.edu.sa']
        self.tags = {'slurm','acceptance','cpu'}
































