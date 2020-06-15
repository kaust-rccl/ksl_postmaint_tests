import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.required_version('>=2.20-dev2')
@rfm.parameterized_test(['single'], ['multi'])
class sing_mpi_hello(rfm.RunOnlyRegressionTest):
    def __init__(self,scale):
        self.maintainers = ['amr.radwan@kaust.edu.sa']
        self.tags = {'sing_mpi_hello'}
        self.valid_systems = ['ibex:batch_nompi']
        self.valid_prog_environs = ['gnu']
        #self.sourcesdir= os.path.join(self.current_system.resourcesdir,'singularity')
        self.sourcesdir= None
        self.pre_run  = ['XDG_RUNTIME_DIR=${PWD} singularity pull docker://amrradwan/ompi-400-ubuntu-18'] 
        self.sanity_patterns = sn.assert_found(r'^Hello world', self.stdout)
        if scale == 'single':
            self.descr = 'Singularity MPI Hello on Single Node'
            self.modules=['singularity/3.5']
            self.num_tasks = 4
            self.num_tasks_per_node = 4
            self.executable = 'singularity exec ompi-400-ubuntu-18_latest.sif mpirun /opt/mpi_hello_world'

        else:
            self.descr = 'Singularity MPI Hello on Multi Node'
            self.modules=['singularity/3.5','openmpi/4.0.1/gnu-6.4.0']
            self.num_tasks = 4
            self.num_tasks_per_node = 2
            self.executable = 'mpirun singularity exec ompi-400-ubuntu-18_latest.sif /opt/mpi_hello_world'

