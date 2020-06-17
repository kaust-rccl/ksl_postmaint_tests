# An example of system check where the mpi launcher is omitted in the jobscript.
import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.parameterized_test(['avail'],['load'],['purge'])
class fs_check(rfm.RunOnlyRegressionTest):
    def __init__(self,variant):
        super().__init__()
        self.descr = 'Module system check on ilogin and compute nodes'
        self.valid_systems = ['ibex:login','ibex:batch_nompi']
        self.valid_prog_environs = ['builtin-gcc']
        self.sourcesdir=None
        self.num_tasks=1
        if variant == "avail":
            self.executable='echo $MODULEPATH'
            self.sanity_patterns =sn.assert_found(r'/sw/csi/modulefiles/applications:/sw/csi/modulefiles/compilers:/sw/csi/modulefiles/libs:/sw/services/modulefiles',self.stdout)
        elif variant == "load":
            self.executable='module load git'	
            self.sanity_patterns =sn.assert_found(r'Git 2.15.0 is now loaded',self.stderr)
        elif variant == "purge":
            self.pre_run = ['module load git','module purge']
            self.executable='module list'
            self.sanity_patterns =sn.assert_found(r'No Modulefiles Currently Loaded.',self.stderr)

        self.maintainers = ['mohsin.shaikh@kaust.edu.sa']
        self.tags = {'modulesystem'}

































