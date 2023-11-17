import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class nccl_tests(rfm.RunOnlyRegressionTest):

      variant= parameter(['v100_8_singlenode','v100_4_singlenode','v100_8_multinode','a100_4_singlenode','a100_4_multinode','a100_8_singlenode','a100_8_multinode'])


           ## TEST BASIC INFO
      maintainers = ['rana.selim@kaust.edu.sa']
      descr = 'running nccl tests'

           ## SETTING TEST ENV
      sourcesdir= '../src/env'
      valid_prog_environs = ['gpustack_builtin']
      valid_systems = ['ibex:batch']
      modules = ['openmpi/4.1.4/gnu11.2.1-cuda11.8','cuda/11.8','nccl/2.17.1-cuda11.8']
      reference = {
                        'ibex' : {
                                'v100_8_singlenode' : (100,-0.1,None,'GB/s'),
                                'v100_4_singlenode' : (100,-0.1,None,'GB/s'),
                                'a100_4_singlenode' :(150,-0.1,None,'GB/s'),
                                'a100_8_singlenode':(150,-0.1,None,'GB/s'),
                                'v100_8_multinode' : (13,-0.1,None,'GB/s'),
                                'a100_4_multinode' : (40,-0.1,None,'GB/s'),
                                'a100_8_multinode' : (100,-0.1,None,'GB/s')


                        }
                }
      
          ## RUN AND VALIDATE
      @run_after('init')
      def setting_variables(self):
        if self.variant == 'v100_4_singlenode': 
           self.time_limit = '30m'
           self.num_tasks=1
           self.prerun_cmds = ['./env.sh']
           self.extra_resources = {'memory': {'size': '700G'}}          
           self.executable='all_reduce_perf -g 4 -o all -c 1 -f 2 -d all'
           self.num_cpus_per_task=30
           self.num_gpus_per_node=4
           self.extra_resources = {'constraint': {'type': 'gpu_v100'}}
        elif self.variant == 'v100_8_singlenode':
           self.time_limit = '30m'
           self.num_tasks=1
           self.extra_resources = {'memory': {'size': '700G'}}
           self.prerun_cmds = ['./env.sh']
           self.executable='all_reduce_perf -g 8 -o all -c 1 -f 2 -d all'
           self.num_cpus_per_task=46
           self.num_gpus_per_node=8
           self.extra_resources = {'constraint': {'type': 'v100'}}
        elif self.variant == 'a100_8_singlenode':
           self.time_limit = '30m'
           self.num_tasks=1
           self.prerun_cmds = ['./env.sh']
           self.executable='all_reduce_perf -g 8 -o all -c 1 -f 2 -d all'
           self.num_cpus_per_task=46
           self.num_gpus_per_node=8
           self.extra_resources = {'constraint': {'type': 'a100'}}
        elif self.variant == 'v100_8_multinode':
           self.num_tasks=2
           self.time_limit = '2h'
           self.extra_resources = {'constraint': {'type': 'v100'}}
           self.num_cpus_per_task=46
           self.prerun_cmds = ['./env.sh']
           self.executable='srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} --cpu-bind=cores    all_reduce_perf -b 8 -e 256M -f 2 -g 8 -c 1 -n 50 -w 20'
           self.prerun_cmds = ['export NCCL_DEBUG=INFO','export UCX_TLS=tcp','hostname','module list']
        elif self.variant == 'a100_4_singlenode':
           self.time_limit = '30m'
           self.num_tasks=1
           self.executable='all_reduce_perf -g 4 -o all -c 1 -f 2 -d all'
           self.num_cpus_per_task=32
           self.num_gpus_per_node=4
           self.prerun_cmds = ['./env.sh']
           self.extra_resources = {'constraint': {'type': 'gpu_a100'}}
        elif  self.variant == 'a100_4_multinode':
           self.num_tasks=8
           self.time_limit = '2h'
           self.extra_resources = {'constraint': {'type': 'a100,4gpus'}}
           self.num_cpus_per_task=15
           self.executable='srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} --cpu-bind=map_cpu:32,47,5,20 all_reduce_perf -b 4G -e 4G  -g 1  -n 100 -w 50 -f 2 -p 0 -z 0 -c 1'
           self.prerun_cmds = ['export NCCL_DEBUG=INFO','export NCCL_IB_HCA=mlx5_0:1,mlx5_1:1','export NCCL_ALGO=Tree','export NCCL_NET_GDR_LEVEL=5','hostname','module list','./env']
        elif self.variant == 'a100_8_multinode':

           self.num_tasks=16
           self.time_limit = '2h'
           self.extra_resources = {'constraint': {'type': 'a100,8gpus'}}
           self.num_cpus_per_task=15
           self.executable='srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} --cpu-bind=cores    all_reduce_perf -b 4G -e 4G  -g 1  -n 100 -w 50 -f 2 -p 0 -z 0 -c 1'
           self.prerun_cmds = ['export NCCL_DEBUG=INFO','export NCCL_ALGO=Tree','export NCCL_NET_GDR_LEVEL=5','hostname','module list','./env']
     

       

        self.tags = {'gpu',self.variant,'acceptance','nccl'}

                
    


      @run_before('run')
      def set_job_options(self):
        if self.variant== 'v100_8_multinode':
           self.job.options = ['--gpus=16','--gpus-per-node=8']
        elif self.variant== 'a100_4_multinode':
           self.job.options = ['--gpus=8','--gpus-per-node=4']
        elif self.variant== 'a100_8_multinode':
           self.job.options = ['--nodes=2','--gpus=16','--gpus-per-node=8']



      @run_before('sanity')
      def set_sanity_patterns(self):
          self.sanity_patterns = sn.assert_found(r'# Avg bus bandwidth', self.stdout)
         

      @run_before('performance')
      def set_perf_patterns(self):
          self.perf_patterns = {self.variant : sn.extractsingle(r'^#\s[A]\w+\s\w+\s\w+\s+[:]\s(?P<Busbw>\d*\.\d+)', self.stdout, 'Busbw' , float)}
