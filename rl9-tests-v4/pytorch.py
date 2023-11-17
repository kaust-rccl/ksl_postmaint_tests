import os
import reframe as rfm
import reframe.utility.sanity as sn

class pytorch_test(rfm.RunOnlyRegressionTest):
      maintainers = ['rana.selim@kaust.edu.sa']
      descr = 'running pytorch tests for v100 and a100 gpus'
      tags = {'pytorch','gpu'}
      sourcesdir= '../src/pytorch/a100'
      valid_systems = ['ibex:batch']
      valid_prog_environs = ['gpustack_builtin']
      
      @run_before('sanity')
      def set_sanity_patterns(self):
          self.sanity_patterns = sn.assert_found(r'Epoch_time', self.stdout)

 
      @run_before('performance')
      def set_perf_patterns(self):
          self.perf_patterns = {self.variant: sn.extractsingle(r'^[E]\w+[_]\w+[:]\s+(?P<Epoch_time>\d*\.\d+)',self.stdout, 'Epoch_time', float)}
                
                
@rfm.simple_test
class pytorch_a100_gpu(pytorch_test):
      variant= parameter(['a100_8_singlenode', 'a100_4_singlenode','a100_8_4GPUS_singlenode'])
      valid_systems = ['ibex:batch']
      time_limit = "3h"  
      reference = {
                        'ibex' : {
                                'a100_8_singlenode' : (1100,None,+10,None),
                                'a100_4_singlenode' : (2200,None,+10,None),
                                'a100_8_4GPUS_singlenode' : (2100,None,+10,None)
                               
                        }
                }
      
      @run_after('init')
      def setting_variables(self):
          self.tags |= {'a100' , self.variant}
          self.prerun_cmds= ['module purge','module load rl9-gpustack','module use  /sw/rl9g/dl/modulefiles ',
                             'module load  horovod/0.28.0',
                             'export OMPI_MCA_btl_openib_warn_no_device_params_found=0',
                             'export UCX_MEMTYPE_CACHE=n','export UCX_TLS=tcp',
                             'export DATA_DIR="/ibex/ai/reference/CV/ILSVR/classification-localization/data/jpeg/"',
                             'export main_exe="./train_resnet50.py"','batch_size=256',
                             'epochs=5', 'export workers=${SLURM_CPUS_PER_TASK}','module list',
                             'export cmd="python3 ${main_exe} --epochs ${epochs} --batch-size ${batch_size} --num_workers=$workers --root-dir=${DATA_DIR} --train-dir ${DATA_DIR}/train --val-dir ${DATA_DIR}/val ${NODE_LOCAL_STORAGE}"']
          
          self.executable= 'time -p srun -u -n ${SLURM_NTASKS} -N ${SLURM_NNODES} -c ${SLURM_CPUS_PER_TASK} ${cmd} --log-dir=log.${SLURM_JOBID} --warmup-epochs=0.0'
          
          if self.variant == 'a100_8_singlenode':
             self.num_tasks= 8
             self.num_cpus_per_task=5
             self.extra_resources = {'constraint': {'type': 'a100,8gpus'},'memory': {'size': '400G'}}
             self.num_gpus_per_node=8
          elif self.variant == 'a100_4_singlenode':
             self.num_tasks= 4
             self.num_cpus_per_task=5
             self.extra_resources = {'constraint': {'type': 'a100,4gpus'},'memory': {'size': '400G'}}
             self.num_gpus_per_node=4
          elif self.variant == 'a100_8_4GPUS_singlenode':
             self.num_tasks= 4
             self.num_cpus_per_task=5
             self.extra_resources = {'constraint': {'type': 'a100,8gpus'},'memory': {'size': '400G'}}
             #self.num_gpus_per_node=8
      
      
      @run_before('run')
      def set_job_options(self):
        if self.variant == 'a100_8_4GPUS_singlenode':
          self.job.options = ['--gpus=4',
                              '--gpus-per-node=4',
                              '--gpus-per-socket=4',
                              '--sockets-per-node=1'
                              ]

  
     
     
@rfm.simple_test
class pytorch_v100_gpu(pytorch_test):
      variant = parameter(['v100_8_singlenode' , 'v100_8_multinode'])
      time_limit= '2h'
      reference = {
                        'ibex' : {
                                'v100_8_singlenode' : (1100,None,+10,None),
                                'v100_8_multinode'  : (1100,None,+10,None)
                        }
                }
      
      @run_after('init')
      def setting_variables(self):
        self.tags |= {'v100' , self.variant}
        self.extra_resources = {'constraint': {'type': 'v100,gpu_ai'},'memory': {'size': '700G'}}
        self.prerun_cmds= ['module purge','module load rl9-gpustack','module use  /sw/rl9g/dl/modulefiles ',
                             'module load  horovod/0.28.0',
                             'export OMPI_MCA_btl_openib_warn_no_device_params_found=0',
                             'export UCX_MEMTYPE_CACHE=n','export UCX_TLS=tcp',
                             'export DATA_DIR="/ibex/ai/reference/CV/ILSVR/classification-localization/data/jpeg/"',
                             'export main_exe="./train_resnet50.py"','batch_size=256',
                             'epochs=5', 'export workers=${SLURM_CPUS_PER_TASK}','module list',
                             'export cmd="python3 ${main_exe} --epochs ${epochs} --batch-size ${batch_size} --num_workers=$workers --root-dir=${DATA_DIR} --train-dir ${DATA_DIR}/train --val-dir ${DATA_DIR}/val ${NODE_LOCAL_STORAGE}"']

        self.executable= 'time -p srun -u -n ${SLURM_NTASKS} -N ${SLURM_NNODES} -c ${SLURM_CPUS_PER_TASK} ${cmd} --log-dir=log.${SLURM_JOBID} --warmup-epochs=0.0'  
        
        if self.variant == 'v100_8_singlenode': 
           self.num_tasks=8
           self.num_cpus_per_task=5
           

        elif  self.variant == 'v100_8_multinode':
           self.num_tasks= 16
           self.num_cpus_per_task=6
               

      @run_before('run')
      def set_job_options(self):
        if self.variant== 'v100_8_singlenode':
           self.job.options = ['--gpus=8',
                              '--gpus-per-node=8',
                             # '--account=ibex-cs'
                             ]
                              
        elif self.variant == 'v100_8_multinode':
           self.job.options = ['--gpus=16',
                              '--gpus-per-node=4',
                             # '--account=ibex-cs'
                             ]
