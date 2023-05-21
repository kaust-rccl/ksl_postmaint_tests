import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class Cuda_device_checks(rfm.RegressionTest):
      variant= parameter(['v100_4','v100_8', 'p100','rtx2080ti'])

      @rfm.run_after('init')
      def setting_variables(self):
        self.descr = 'CUDA Device query'
        self.constraint = self.variant
        # Environment settings
        self.valid_systems = ['ibex:batch']
        self.valid_prog_environs = ['gpustack_cuda']
        self.sourcesdir= '../src/cuda/device_check'
        self.time_limit = '10m'
        if self.variant == 'v100_8' or self.variant == 'rtx2080ti' :
           self.num_gpus_per_node=8
        else:
           self.num_gpus_per_node=4

        # Resource and runtime settings
       
        #self.num_tasks=1
        
        self.num_tasks=1

        # Build source using makefile provided in the resourcesdir
        self.build_system='Make'
        # In the run phase invoke the executable name as below
        self.prerun_cmds = ['./env.sh']
        self.executable='./a.out'
        if self.variant == 'v100_4' or self.variant == 'v100_8':
           self.extra_resources = {'constraint': {'type': 'v100'}}
        elif self.variant == 'p100':
           self.extra_resources = {'constraint': {'type': 'p100'}}
        elif self.variant == 'rtx2080ti':
           self.extra_resources = {'constraint': {'type': 'rtx2080ti'}}




        #Validation
        self.sanity_patterns = sn.assert_found (r'Devcount' , self.stdout)
        # Performance check
         
        self.perf_patterns = {self.variant : 
                sn.extractsingle(r'Devcount\s+(?P<devices>\S+)', self.stdout, 'devices', int)}
        self.reference = {
                            'ibex' : {      'p100': (4,None,None,None),
                                            'v100_4': (4,None,None,None),
                                            'v100_8': (8,None,None,None),
                                            'rtx2080ti': (8,None,None,None)
                                            },
                            }
        self.tags = {'gpu',self.variant,'acceptance','device_query','cuda'}

        self.maintainers = ['mohsin.shaikh@kaust.edu.sa']
        
