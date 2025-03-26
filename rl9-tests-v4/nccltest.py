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
                                'a100_4_singlenode' :(230,-0.1,None,'GB/s'),
                                'a100_8_singlenode':(230,-0.1,None,'GB/s'),
                                'v100_8_multinode' : (100,-0.1,None,'GB/s'),
                                'a100_4_multinode' : (40,-0.1,None,'GB/s'),
                                'a100_8_multinode' : (100.0,-0.1,None,'GB/s')
                        }
                }
      
          ## RUN AND VALIDATE
      @run_after('init')
      def setting_variables(self):
        if self.variant == 'v100_4_singlenode': 
           self.time_limit = '30m'
           self.num_tasks=4
           self.tasks-per-node=4
           self.num_cpus_per_task=7
           self.num_gpus_per_node=4
           self.prerun_cmds = ['./env.sh']
           self.extra_resources = {'memory': {'size': '300G'}}          
           self.executable='srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} -c ${SLURM_CPUS_PER_TASK} all_reduce_perf -b 4G -e 4G -f 2 -g 1 -c 0 -n 50 -w 20'
           self.extra_resources = {'constraint': {'type': 'v100,cpu_intel_gold_6142'}}
        elif self.variant == 'v100_8_singlenode':
           self.time_limit = '30m'
           self.num_tasks=8
           self.tasks-per-node=8
           self.num_cpus_per_task=5
           self.num_gpus_per_node=8
           self.extra_resources = {'memory': {'size': '700G'}}
           self.prerun_cmds = ['./env.sh']
           self.executable='srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} -c ${SLURM_CPUS_PER_TASK} all_reduce_perf -b 4G -e 4G -f 2 -g 1 -c 0 -n 50 -w 20 '
           self.extra_resources = {'constraint': {'type': 'v100'}}
        elif self.variant == 'a100_8_singlenode':
           self.time_limit = '30m'
           self.num_tasks=8
           self.tasks-per-node=8
           self.num_cpus_per_task=15
           self.num_gpus_per_node=8
           self.prerun_cmds = ['./env.sh']
           self.executable='srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} -c ${SLURM_CPUS_PER_TASK} all_reduce_perf -b 4G -e 4G -f 2 -g 1 -c 0 -n 50 -w 20'
           self.extra_resources = {'constraint': {'type': 'a100'}}
        elif self.variant == 'v100_8_multinode':
           self.num_tasks=16
           self.tasks-per-node=8
           self.time_limit = '30m'
           self.extra_resources = {'constraint': {'type': 'v100,gpu_ai'}}
           self.num_cpus_per_task = 5
           self.executable='srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} -c ${SLURM_CPUS_PER_TASK} --cpu-bind=map_cpu:0,6,11,19,24,29,33,38 all_reduce_perf -b 4G -e 4G -f 2 -g 1 -c 0 -n 50 -w 20'
           self.prerun_cmds = ['./env.sh',
                               'export NCCL_DEBUG=INFO',
                               'export NCCL_ALGO=Tree',
                               'export NCCL_NET_GDR_LEVEL=4',
                               'export NCCL_IB_HCA=mlx5',
                               'echo ${SLURM_NODELIST}','module list']
        elif self.variant == 'a100_4_singlenode':
           self.time_limit = '30m'
           self.num_tasks=4
           self.tasks-per-node=4
           self.executable='srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} -c ${SLURM_CPUS_PER_TASK} all_reduce_perf -b 4G -e 4G -f 2 -g 1 -c 0 -n 50 -w 20'
           self.num_cpus_per_task=15
           self.num_gpus_per_node=4
           self.prerun_cmds = ['./env.sh']
           self.extra_resources = {'constraint': {'type': 'a100,4gpus'}}
        elif  self.variant == 'a100_4_multinode':
           self.num_tasks=8
           self.tasks-per-node=4
           self.num_cpus_per_task=15
           self.time_limit = '30m'
           self.extra_resources = {'constraint': {'type': 'a100,4gpus'}}
           self.executable='srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} -c ${SLURM_CPUS_PER_TASK} --cpu-bind=map_cpu:35,45,4,25 all_reduce_perf -b 4G -e 4G -f 2 -g 1 -c 0 -n 50 -w 20'
           self.prerun_cmds = ['export NCCL_DEBUG=INFO',
                               'echo ${SLURM_NODELIST}','module list',
                               'export NCCL_ALGO=Tree',
                               'export NCCL_NET_GDR_LEVEL=4',
                               'export NCCL_IB_HCA=mlx5'
                               ]

        elif self.variant == 'a100_8_multinode':
           self.num_tasks=16
           self.tasks-per-node=8
           self.num_cpus_per_task=15
           self.time_limit = '30m'
           self.extra_resources = {'constraint': {'type': 'a100,8gpus'}}
           self.executable='srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} -c ${SLURM_CPUS_PER_TASK} --cpu-bind=map_cpu:35,45,4,25,105,115,75,85 all_reduce_perf -b 4G -e 4G -f 2 -g 1 -c 0 -n 50 -w 20'
           self.prerun_cmds = ['export NCCL_DEBUG=INFO',
                               'export NCCL_ALGO=Tree',
                               'export NCCL_NET_GDR_LEVEL=4',
                               'export NCCL_IB_HCA=mlx5',
                               'echo ${SLURM_NODELIST}','module list']
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
