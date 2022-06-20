# An example of system check where the mpi launcher is omitted in the jobscript.
import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.simple_test
class modulesystem(rfm.RunOnlyRegressionTest):

      variant= parameter(['avail','load','purge'])
      valid_systems = ['ibex:login','ibex:batch']
      valid_prog_environs = ['cpustack_builtin']
      sourcesdir=None
      num_tasks=1
      time_limit='3m'
      tags={'module'}

      @rfm.run_after('init')
      def setting_variables(self):

        if self.variant == "avail":
            self.executable='echo $MODULEPATH'
            self.sanity_patterns =sn.assert_found(r'/sw/csi/modulefiles/applications:/sw/csi/modulefiles/compilers:/sw/csi/modulefiles/libs:/sw/services/modulefiles',self.stdout)
        elif self.variant == "load":
            self.executable='module load git'	
            self.sanity_patterns =sn.assert_found(r'Git 2.15.0 is now loaded',self.stderr)
        elif self.variant == "purge":
            self.prerun_cmds = ['module load git','module purge']
            self.executable='module list'
            self.sanity_patterns =sn.assert_found(r'No Modulefiles Currently Loaded.',self.stderr)
      

































