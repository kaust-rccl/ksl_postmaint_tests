import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.parameterized_test(['v100'],['p100'],['rtx2080ti'])
class Cuda_perf_checks(rfm.RegressionTest):
    def __init__(self, variant):
        
        self.descr = 'CUDA Perf test'
        self.constraint = variant
        # Environment settings
        self.valid_systems = ['ibex:batch','ibex:debug','ibex:gpu_wide']
        self.valid_prog_environs = ['gnu_cuda']
        self.sourcesdir=os.path.join(self.current_system.resourcesdir,'cuda/perf_check')
        
        # Resource and runtime settings
       
        #self.num_tasks=1
        self.num_gpus_per_node = 1
        self.num_tasks=1

        # Build source using makefile provided in the resourcesdir
        self.build_system='Make'
        # In the run phase invoke the executable name as below
        self.executable='a.out'
        self.executable_opts = ['4096','1000']
        #Validation
        self.sanity_patterns = sn.assert_found (r'time for single matrix vector multiplication' , self.stdout)
        # Performance check
         
        self.perf_patterns = {variant : 
                sn.extractsingle(r'Performance:\s+(?P<Gflops>\S+) Gflop/s', self.stdout, 'Gflops', float)}
        self.reference = {
                            'ibex' : {      'p100': (6.6,-0.1,None),
                                            'v100': (60.0,-0.1,None),
                                            'rtx2080ti': (6.6,-0.1,None)
                                            },
                            }
        self.tags = {'cuda',variant,'acceptance'}

        self.maintainers = ['mohsin.shaikh@kaust.edu.sa']
        
    def setup(self,partition,environ,**job_opts):
        super().setup(partition,environ,**job_opts)
        self.job.options = [ '--gres=gpu:%s:%d' % (self.constraint,self.num_gpus_per_node)]


