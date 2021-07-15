import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class license_check(rfm.RegressionTest):
      @rfm.run_after('init')
      def setting_variables(self):
        self.valid_systems = ['ibex:login','ibex:batch']
        self.descr = 'License check test by compiling a code using intel'
        self.valid_prog_environs = ['cpustack_intel']
        self.sourcesdir='../src/license'
        self.build_system='Make'
        self.executable='./a.out'

        # Job script attributes
        self.time_limit = '10m' #is a tuple in the format (H,M,S)
        self.num_tasks = 1
        self.num_cpus_per_task=1
        
        self.sanity_patterns = sn.assert_found(r'70', self.stdout)
        
        # tags are useful to filter tests when not all but specific the tests are suppose to run
        self.tags = {'license_check'}


