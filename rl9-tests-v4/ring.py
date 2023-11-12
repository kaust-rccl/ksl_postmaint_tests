import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.simple_test
class ring_check(rfm.RegressionTest):
      variant= parameter(['openmpi','intelmpi'])
      @run_after('init')
      def setting_variables(self):
        self.descr = 'Ring of MPI tasks in Cart Comm'
        self.valid_systems = ['ibex:batch']
        self.valid_prog_environs = ['cpustack_openmpi','cpustack_intelmpi']
        self.sourcesdir='../src/ring'
        self.prerun_cmds = ['./env.sh']
        self.executable='./ring'
        self.executable_opts = ['1024', '10']
        self.build_system = 'Make'
        
        self.sanity_patterns = sn.assert_found(
            r'MPI ring test with Cartesian communicator', self.stdout)
        self.time_limit='10m'
        self.num_tasks = 4
        self.num_tasks_per_node = 4

        if self.variant == 'openmpi':
           self.valid_prog_environs = ['cpustack_openmpi']
        elif self.variant == 'intelmpi':
           self.valid_prog_environs = ['cpustack_intelmpi']
           self.prerun_cmds = ['export FI_PROVIDER=verbs']


        self.maintainers = ['MS']
        self.tags = {'ring','cpu'}
