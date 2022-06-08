import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class nccl_tests(rfm.RunOnlyRegressionTest):

      variant= parameter(['v100_8_singlenode', 'v100_8_multinode','a100_8_singlenode','a100_8_multinode'])


           ## TEST BASIC INFO
      maintainers = ['rana.selim@kaust.edu.sa']
      descr = 'running nccl tests'

      tags = {'gpu','nccl'}

           ## SETTING TEST ENV
      sourcesdir= None
      valid_prog_environs = ['gpustack_builtin']
      valid_systems = ['ibex:batch']
      modules = ['dl','cuda/10.2.89','openmpi/4.0.3-cuda10.2','nccl/2.7.3.1']
      reference = {
                        'ibex' : {
                                'v100_8_singlenode' : (100,None,+2,'GB/s'),
                                'a100_8_singlenode' :(150,None,+2,'GB/s'),
                                'v100_8_multinode' : (13.00000,None,+2,'GB/s'),
                                'a100_8_multinode' : (13.00000,None,+2,'GB/s')

                        }
                }
      
          ## RUN AND VALIDATE
      @rfm.run_after('init')
      def setting_variables(self):
        if self.variant == 'v100_8_singlenode': 
           self.time_limit = '30m'
           self.num_tasks=1
           self.extra_resources = {'memory': {'size': '700G'}}          
           self.executable='all_reduce_perf -g 8 -o all -c 1 -f 2 -d all'
           self.num_cpus_per_task=46
           self.num_gpus_per_node=8
           self.extra_resources = {'constraint': {'type': 'v100'}}

        elif self.variant == 'a100_8_singlenode':
           self.time_limit = '30m'
           self.num_tasks=1
           self.executable='all_reduce_perf -g 8 -o all -c 1 -f 2 -d all'
           self.num_cpus_per_task=46
           self.num_gpus_per_node=8
           self.extra_resources = {'constraint': {'type': 'a100'}}

        
             
        elif self.variant == 'v100_8_multinode':

           self.num_tasks=2
           self.time_limit = '2h'
           self.extra_resources = {'constraint': {'type': 'v100'}}
           self.num_cpus_per_task=46
           self.executable='srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} --cpu-bind=cores    all_reduce_perf -b 8 -e 256M -f 2 -g 8 -c 1 -n 50 -w 20'
           self.prerun_cmds = ['export NCCL_DEBUG=INFO','export UCX_TLS=tcp','hostname','module list']
           #self.num_gpus_per_node=8


           self.executable='srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} --cpu-bind=cores  all_reduce_perf -b 8 -e 256M -f 2 -g 8 -c 1 -n 50 -w 20'

           self.prerun_cmds = ['export NCCL_DEBUG=INFO','export UCX_TLS=tcp','hostname','module list']
          # self.num_gpus_per_node=8


        self.tags = {'gpu',self.variant,'acceptance'}

                
    


      @rfm.run_before('run')
      def set_job_options(self):
        if self.variant== 'v100_8_multinode':
           self.job.options = ['--gpus=16','--gpus-per-node=8']
        elif self.variant== 'a100_8_multinode':
           self.job.options = ['--gpus=16','--gpus-per-node=8']



      @rfm.run_before('sanity')
      def set_sanity_patterns(self):
          self.sanity_patterns = sn.assert_found(r'# Avg bus bandwidth', self.stdout)
         

      @rfm.run_before('performance')
      def set_perf_patterns(self):
          self.perf_patterns = {self.variant : sn.extractsingle(r'^#\s[A]\w+\s\w+\s\w+\s+[:]\s(?P<Busbw>\d*\.\d+)', self.stdout, 'Busbw' , float)}
