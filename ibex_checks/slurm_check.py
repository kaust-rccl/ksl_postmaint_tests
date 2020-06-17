import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.parameterized_test(['slurmctld'],['squeue'],['sacct'])
class slurm_check(rfm.RunOnlyRegressionTest):
    def __init__(self,variant):
        super().__init__()
        self.descr = 'SLURM check on ilogin and compute nodes'
        self.valid_systems = ['ibex:login','ibex:batch_nompi']
        self.valid_prog_environs = ['builtin-gcc']
        self.sourcesdir=None
        self.num_tasks=1
        if variant == "slurmctld":
            self.executable='scontrol ping'
            self.sanity_patterns =sn.assert_found(r'slurm209-02 is UP',self.stdout)
        elif variant == "squeue":
            self.executable='squeue -u ismailiy'	
            self.sanity_patterns =sn.assert_found(r'NODELIST',self.stdout)
        elif variant == "sacct":
            self.executable='sacct'
            self.sanity_patterns =sn.assert_found(r'JobID    JobName  Partition    Account  AllocCPUS      State ExitCode',self.stdout)

        self.maintainers = ['mohsin.shaikh@kaust.edu.sa']
        self.tags = {'slurm_check'}

































