import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class pytorch(rfm.RunOnlyRegressionTest):
      variant= parameter(['a100_8_singlenode', 'a100_4_singlenode','a100_8_4GPUS_singlenode'])

      @rfm.run_after('init')
      def setting_variables(self):
           ## TEST BASIC INFO
          self.maintainers = ['rana.selim@kaust.edu.sa']
          self.descr = 'running pytorch test'
          self.tags = {'pytorch',self.variant,'gpu'}
          self.sourcesdir= '../src/pytorch/a100'
          self.valid_prog_environs = ['gpustack_builtin']
          self.valid_systems = ['ibex:batch']
          self.time_limit= '3h'

      
          self.prerun_cmds= ['module purge','module load gpustack','module load cuda/11.2.2','module load dl',
                             'module load pytorch/1.9.0 torchvision  horovod/0.22.1_torch',
                             'export OMPI_MCA_btl_openib_warn_no_device_params_found=0',
                             'export UCX_MEMTYPE_CACHE=n','export UCX_TLS=tcp',
                             'export DATA_DIR="/local/reference/CV/ILSVR/classification-localization/data/jpeg"',
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


      @rfm.run_before('run')
      def set_job_options(self):
        if self.variant == 'a100_8_4GPUS_singlenode':
          self.job.options = ['--gpus=4',
                              '--gpus-per-node=4',
                              '--gpus-per-socket=4',
                              '--sockets-per-node=1'
                              ]


      @rfm.run_before('sanity')
      def set_sanity_patterns(self):
          self.sanity_patterns = sn.assert_found(r'Epoch_time', self.stdout)

         


      @rfm.run_before('performance')
      def set_perf_patterns(self):
          self.perf_patterns = {self.variant: sn.extractsingle(r'^[E]\w+[_]\w+[:]\s+(?P<Eposh_time>\d*\.\d+)',self.stdout, 'Eposh_time', float)}

      # Refrerence according to running training on 16 gpus and can be revised
      reference = {
                        'ibex' : {
                                'a100_8_singlenode' : (1100,None,+10,None),
                                'a100_4_singlenode' : (2600,None,+10,None),
                                'a100_8_4GPUS_singlenode' : (2100,None,+10,None),


                               
                        }
                }
