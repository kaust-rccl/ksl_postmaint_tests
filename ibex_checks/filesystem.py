# An example of system check where the mpi launcher is omitted in the jobscript.
import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.parameterized_test(['home'],['scratch'])
class fs_check(rfm.RunOnlyRegressionTest):
    def __init__(self,variant):
        super().__init__()
        self.descr = 'Filesystem mount check on longin and compute nodes'
        self.valid_systems = ['ibex:login','ibex:batch_nompi']
        self.valid_prog_environs = ['builtin-gcc']
        self.sourcesdir=None
        self.executable='df -h '
        self.num_tasks=1
        if variant == "home":
            self.sanity_patterns =sn.assert_found(r'/home/home',self.stdout)
        elif variant == "scratch":
            self.sanity_patterns =sn.assert_found(r'/scratch/dragon',self.stdout)
        
        self.maintainers = ['mohsin.shaikh@kaust.edu.sa']
        self.tags = {'filesystem'}

































