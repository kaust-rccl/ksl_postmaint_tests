import reframe.utility.sanity as sn
import reframe as rfm

@rfm.parameterized_test(['onenode'],['multinode'])
class mpi_checks(rfm.RunOnlyRegressionTest):
    def __init__(self,variant):
        super().__init__()

        self.time_limit = (0,10,0)

        self.valid_systems = ['ibex:debug']
        self.valid_prog_environs = ['gnu']
        self.sourcesdir= None
        
        self.modules = ['/ibex/scratch/shaima0d/software/modulefiles/osu-microbenchmarks/5.6.2']
        self.executable = 'osu_latency'
        self.executable_opts = ('-m 256:256').split()
        
        if variant == "multinode":
            self.num_tasks=2
            self.num_tasks_per_node=1
        else:
            self.num_tasks=2
            self.num_tasks_per_node=2
        
        self.sanity_patterns = sn.assert_found(r'# OSU MPI Latency Test v5.6.2', self.stdout)
        self.perf_patterns = {
            variant: sn.extractsingle(r'^256\s+(?P<latency>\S+)',
                                     self.stdout, 'latency', float)
        }

        self.reference = {
            'ibex' : {
                'multinode':   (2.0, None, 0.05),
                'onenode': (0.5, None, 0.05),
                    },
#             'ibex:batch' : {
#                 'multinode':   (2.0, None, 0.05),
#                 'onenode': (0.5, None, 0.05),
#                 },
            }
        self.descr = "MPI latency test on two nodes using pre-installed OSU benchmakrs"

        self.maintainer = {'mohsin.shaikh@kaust.edu.sa'}
        self.tags = {'mpi',variant}
