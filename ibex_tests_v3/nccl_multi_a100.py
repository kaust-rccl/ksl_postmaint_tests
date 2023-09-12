import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class nccl_tests(rfm.RunOnlyRegressionTest):

      variant= parameter(['a100_4_multinode','a100_8_multinode'])


           ## TEST BASIC INFO
      maintainers = ['rana.selim@kaust.edu.sa']
      descr = 'running nccl tests'

      #tags = {'gpu','nccl',self.variant}

           ## SETTING TEST ENV
      sourcesdir= '../src/env'
      valid_prog_environs = ['gpustack_builtin']
      valid_systems = ['ibex:batch']
      modules = ['dl','cuda/11.7.0','openmpi-gpu/4.1.4','nccl/2.17.1.1']
      reference = {
                        'ibex' : {
                                'a100_4_multinode' : (40.00000,-2,None,'GB/s'),
                                'a100_8_multinode' : (20.00000,-2,None,'GB/s')

                        }
                }
      
          ## RUN AND VALIDATE
      @rfm.run_after('init')
      def setting_variables(self):
        if  self.variant == 'a100_4_multinode':

           self.num_tasks=8
           self.time_limit = '2h'
           self.extra_resources = {'constraint': {'type': 'a100,4gpus'}}
           self.num_cpus_per_task=15
           self.executable='srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} --cpu-bind=map_cpu:32,47,5,20 all_reduce_perf -b 4G -e 4G  -g 1  -n 100 -w 50 -f 2 -p 0 -z 0 -c 1'
           self.prerun_cmds = ['export NCCL_DEBUG=INFO','export NCCL_IB_HCA=mlx5_0:1,mlx5_1:1','export NCCL_ALGO=Tree','export NCCL_NET_GDR_LEVEL=5','hostname','module list','./env']
          # self.num_gpus_per_node=8
          # self.tags = {'gpu','nccl',self.variant}
     
        elif self.variant == 'a100_8_multinode':

           self.num_tasks=2
           self.time_limit = '2h'
           self.extra_resources = {'constraint': {'type': 'a100,8gpus'}}
           self.num_cpus_per_task=46
           self.executable='srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} --cpu-bind=cores  all_reduce_perf -b 4G -e 4G  -g 1  -n 100 -w 50 -f 2 -p 0 -z 0 -c 1'
           self.prerun_cmds = ['export NCCL_DEBUG=INFO','export NCCL_ALGO=Tree','export NCCL_NET_GDR_LEVEL=5','hostname','module list','./env']

        self.tags = {'gpu','nccl',self.variant}


      @rfm.run_before('run')
      def set_job_options(self):
         if  self.variant == 'a100_4_multinode':
           self.job.options = ['--account=c2227','--gpus=8','--gpus-per-node=4']

               

         elif self.variant == 'a100_8_multinode':
            self.job.options = ['--account=c2227','--gpus=16','--gpus-per-node=8']


      @rfm.run_before('sanity')
      def set_sanity_patterns(self):
          self.sanity_patterns = sn.assert_found(r'# Avg bus bandwidth', self.stdout)
         

      @rfm.run_before('performance')
      def set_perf_patterns(self):
          self.perf_patterns = {self.variant : sn.extractsingle(r'^#\s[A]\w+\s\w+\s\w+\s+[:]\s(?P<Busbw>\d*\.\d+)', self.stdout, 'Busbw' , float)}
