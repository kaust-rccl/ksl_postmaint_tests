import os
import reframe as rfm
import reframe.utility.sanity as sn

class gromacs_gpu(rfm.RunOnlyRegressionTest):
    maintainers = ['ahmed.khatab@kaust.edu.sa']
    descr = 'Run Gromacs GPU test'
    valid_systems = ['ibex:batch']
    valid_prog_environs = ['gpustack_builtin']
    sourcesdir = '../src/gromacs_gpu'
    modules = ['gromacs/2025.2/openmpi4.1.4_cuda12.1_nvhpc-25.5']
    time_limit = '10m'

@rfm.simple_test
class gromacs_a100(gromacs_gpu):
    variant = parameter(['a100_1', 'a100_2'])
    
    @run_after('init')
    def setting_variables(self):
     self.tags = {'gpu', 'acceptance', 'gromacs', 'a100', self.variant}
     if self.variant == "a100_1":
        self.num_tasks = 1
        self.num_tasks_per_node = 1
        self.prerun_cmds = ['./env.sh']
        self.executable = 'gmx_mpi mdrun -deffnm topol -nb gpu -pme gpu -update gpu -bonded gpu -nsteps 100000 -resetstep 90000 -noconfout -dlb no -nstlist 300 -pin on'
        self.reference = {
            'ibex:batch': {
                'Elapsed_time': (324, -0.1, None, 'ns/day')
                }
            } 

     elif self.variant == "a100_2":
        self.num_tasks = 2
        self.num_tasks_per_node = 2
        self.prerun_cmds = ['./env.sh','export GMX_ENABLE_DIRECT_GPU_COMM=1','export GMX_GPU_PME_DECOMPOSITION=1']
        self.executable = 'mpirun -np 2 gmx_mpi mdrun -deffnm topol -nb gpu -pme gpu -npme 1 -update gpu -bonded gpu -nsteps 100000 -resetstep 90000 -noconfout -dlb no -nstlist 300 -pin on'
        self.reference = {
            'ibex:batch': {
                'Elapsed_time': (370, -0.1, None, 'ns/day')
             }
            }


     self.sanity_patterns = sn.assert_found(r'Performance:', 'topol.log')
        
    # Extract the second ns/day using a regex
     self.perf_patterns = {
            'Elapsed_time': sn.extractsingle(
                r'Performance:\s*(\d+\.\d+)', 'topol.log', 1, float
            )
        }

    @run_before('run')
    def set_job_options(self):
        if self.variant == "a100_1":
           self.job.options = ['--constraint=a100',
                              '--gpus=1',
                              '--cpus-per-gpu=16',
                              '--mem=80G'
                              ]
        elif self.variant == "a100_2":
             self.job.options = ['--constraint=a100',
                                '--gpus=2',
                                '--cpus-per-gpu=16',
                                '--mem=80G'
                                ]

