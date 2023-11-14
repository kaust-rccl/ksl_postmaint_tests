import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.simple_test
class sing_mpi_hello(rfm.RunOnlyRegressionTest):
      variant= parameter(['single', 'multi'])
      @run_after('init')
      def setting_variables(self):

        self.maintainers = ['amr.radwan@kaust.edu.sa']
        self.tags = {'sing_mpi_hello','cpu','singularity'}
        self.valid_systems = ['ibex:batch']
        self.valid_prog_environs = ['cpustack_gnu']
        #self.sourcesdir= os.path.join(self.current_system.resourcesdir,'singularity')
        self.sourcesdir= '../src/env'
        self.prerun_cmds  = ['XDG_RUNTIME_DIR=${PWD} singularity pull docker://amrradwan/ompi-400-ubuntu-18','env.sh'] 
        self.time_limit='10m'
        self.sanity_patterns = sn.assert_found(r'^Hello world', self.stdout)
        if self.variant == 'single':
            self.descr = 'Singularity MPI Hello on Single Node'
            self.modules=['singularity/3.9.7']
            self.num_tasks = 4
            self.num_tasks_per_node = 4
            self.executable = 'singularity exec ompi-400-ubuntu-18_latest.sif mpirun /opt/mpi_hello_world'

        else:
            self.descr = 'Singularity MPI Hello on Multi Node'
            self.modules=['singularity/3.9.7','openmpi/4.1.4/gnu11.2.1']
            self.num_tasks = 4
            self.num_tasks_per_node = 2
            self.executable = 'mpirun singularity exec ompi-400-ubuntu-18_latest.sif /opt/mpi_hello_world'

