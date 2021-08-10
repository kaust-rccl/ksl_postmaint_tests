# An example of system check where the mpi launcher is omitted in the jobscript.
import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.simple_test
class fs_check(rfm.RunOnlyRegressionTest):
      variant= parameter(['home', 'scratch'])
      @rfm.run_after('init')
      def setting_variables(self):

        self.descr = 'Filesystem mount check on longin and compute nodes'
        self.valid_systems = ['ibex:login','ibex:batch']
        self.valid_prog_environs = ['cpustack_builtin']
        self.sourcesdir=None
        self.executable='mount'
        self.num_tasks=1
        self.time_limit='10m'
        if self.variant == "home":
            self.sanity_patterns =sn.assert_found(r'/home/home',self.stdout)
        elif self.variant == "scratch":
            self.sanity_patterns =sn.assert_found(r'/ibex/scratch',self.stdout)
        
        self.maintainers = ['mohsin.shaikh@kaust.edu.sa']
        self.tags = {'filesystem'}

































