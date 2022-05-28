import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class Cuda_perf_checks(rfm.RegressionTest):
      variant= parameter(['v100_4','v100_8', 'p100','rtx2080ti','a100_4','a100_8'])

      @rfm.run_after('init')
      def setting_variables(self):
        self.descr = 'CUDA Perf test'
        self.constraint = self.variant
        # Environment settings
        self.valid_systems = ['ibex:batch']
        self.valid_prog_environs = ['gpustack_cuda']
        self.sourcesdir= '../src/cuda/perf_check'
        self.time_limit = '10m'
        self.num_gpus_per_node=1

        # Resource and runtime settings
       
        #self.num_tasks=1
        
        self.num_tasks=1

        # Build source using makefile provided in the resourcesdir
        self.build_system='Make'
        # In the run phase invoke the executable name as below
        self.executable='./a.out'
        self.executable_opts = ['4096','1000']
        if self.variant == 'v100_4':
           self.extra_resources = {'constraint': {'type': 'v100,cpu_intel_gold_6142'}}
        elif self.variant == 'v100_8':
           self.extra_resources = {'constraint': {'type': 'v100,gpu_ai'}}
        elif self.variant == 'p100':
           self.extra_resources = {'constraint': {'type': 'p100'}}
        elif self.variant == 'rtx2080ti':
           self.extra_resources = {'constraint': {'type': 'rtx2080ti'}}
        elif self.variant == 'a100_4':
           self.extra_resources = {'constraint': {'type': 'a100,4gpus'}}
        elif self.variant == 'a100_8':
           self.extra_resources = {'constraint': {'type': 'a100,8gpus'}}




        #Validation
        self.sanity_patterns = sn.assert_found (r'time for single matrix vector multiplication' , self.stdout)
        # Performance check
         
        self.perf_patterns = {self.variant : 
                sn.extractsingle(r'Performance:\s+(?P<Gflops>\S+) Gflop/s', self.stdout, 'Gflops', float)}
        self.reference = {
                            'ibex' : {      'p100': (6.6,-0.1,None,None),
                                            'v100_4': (53,-0.1,None,None),
                                            'v100_8': (53,-0.1,None,None),
                                            'rtx2080ti': (6.6,-0.1,None,None),
                                            'a100_4': (38,-0.1,None,None),
                                            'a100_8': (38,-0.1,None,None)
    },
                            }
        self.tags = {'gpu',self.variant,'acceptance'}

        self.maintainers = ['mohsin.shaikh@kaust.edu.sa']
       
