import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.required_version('>=2.20-dev2')
@rfm.simple_test
class singularity_checks(rfm.RunOnlyRegressionTest):
    def __init__(self):
        self.descr = 'Run commands inside a container'
        self.valid_systems = ['ibex:batch']
        self.valid_prog_environs = ['gnu']

        self.sourcesdir=os.path.join(self.current_system.resourcesdir,'singularity')
        
        self.modules=['singularity/3.5']
        self.num_tasks=4
        self.num_tasks_per_node=4
        
        self.pre_run  = ['XDG_RUNTIME_DIR=${PWD} singularity pull docker://mshaikh/hpl_mpich314:latest; export SINGULARITYENV_LD_LIBRARY_PATH=/software/lib:$LD_LIBRARY_PATH;export SINGULARITYENV_PATH=/software/bin:$_PATH']

        self.executable = 'singularity exec hpl_mpich314_latest.sif /hpl/bin/ubuntu/xhpl'
        
    
        self.sanity_patterns = sn.assert_found(r'^HPLinpack 2.3  --  High-Performance Linpack benchmark', self.stdout)
        self.perf_patterns = {
#            'perf': sn.extractsingle(r'^WR\w+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\S+\s+(?P<latency>\S+)',
#                                     self.stdout, 'GFlops', float)
            'perf': sn.extractsingle(r'^WR\w+\s+(?P<latency>\S+)',
                                     self.stdout, 'GFlops', str)
        }
        self.reference = {
            'ibex' : {
                'perf': (3.6468, -0.05, None),
                    },
            }        
        self.maintainers = ['mohsin.shaikh@kaust.edu.sa']
        self.tags = {'singularity'}
