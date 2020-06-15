import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class license_check(rfm.RegressionTest):
    def __init__(self,**kwargs):
        super().__init__()
        self.valid_systems = ['ibex:login','ibex:batch_nompi']
        self.descr = 'License check test by compiling a code using intel'
        self.valid_prog_environs = ['intel']
        self.modules=['intel/2019']
        # note that resourcesdir is definted as $PWD/resourcesdir if RESORUCES_DIR variable has not been set
        self.sourcesdir=os.path.join(self.current_system.resourcesdir,'license')
        self.build_system='Make'
        self.executable='./a.out'

        # Job script attributes
        self.modules=['intel/2019']
        self.time_limit = (0,10,0)  #is a tuple in the format (H,M,S)
        self.num_tasks = 1
        self.num_cpus_per_task=1
        
        self.sanity_patterns = sn.assert_found(r'70', self.stdout)
        
        # tags are useful to filter tests when not all but specific the tests are suppose to run
        self.tags = {'license_check'}


