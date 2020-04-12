import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.simple_test
class ring_check(rfm.RegressionTest):
    def __init__(self,**kwargs):
        self.descr = 'Ring of MPI tasks in Cart Comm'
        self.valid_systems = ['ibex']
        self.valid_prog_environs = ['gnu','intel']
        self.sourcesdir=os.path.join(self.current_system.resourcesdir,'ring')
        
        self.executable='ring'
        self.executable_opts = ['1024', '10']
        self.build_system = 'Make'
     

        self.sanity_patterns = sn.assert_found(
            r'MPI ring test with Cartesian communicator', self.stdout)
        
        self.num_tasks = 4
        self.num_tasks_per_node = 4 
            
        self.maintainers = ['MS']
        self.tags = {'ring'}

