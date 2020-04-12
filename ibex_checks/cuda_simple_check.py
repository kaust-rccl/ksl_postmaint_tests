import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.simple_test
class cuda_simple_check(rfm.RegressionTest):
    def __init__(self):
        super().__init__()
        self.descr = 'Matrix-vector multiplication example with CUDA'
        self.valid_systems = ['ibex']
        self.valid_prog_environs = ['gnu_cuda']
        self.sourcesdir=os.path.join(self.current_system.resourcesdir,'cuda/simple_check')
        self.executable='a.out'
        self.executable_opts = ['1024', '100']
        self.num_tasks=1
        self.num_gpus_per_node = 1
        self.sanity_patterns = sn.assert_found(
            r'time for single matrix vector multiplication', self.stdout)
        self.maintainers = ['you-can-type-your-email-here']
        self.tags = {'cuda_simple'}