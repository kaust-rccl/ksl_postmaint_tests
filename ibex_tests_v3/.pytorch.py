import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class pytorch(rfm.RunOnlyRegressionTest):
      variant= parameter(['v100_8_singlenode', 'v100_8_multinode','a100_8_singlenode','a100_4_singlenode'])
      @rfm.run_after('init')
      def setting_variables(self):
           ## TEST BASIC INFO
          self.maintainers = ['rana.selim@kaust.edu.sa']
          self.descr = 'running pytorch test'
          self.tags = {'gpu',self.variant,'acceptance'}
    
               ## SETTING TEST ENV
          self.sourcesdir= '../src/pytorch'
          self.valid_prog_environs = ['gpustack_builtin']
          self.valid_systems = ['ibex:batch']
          #self.modules = ['']
          #self.num_tasks= 16
          #self.num_cpus_per_task=6

          #self.extra_resources = {'constraint': {'type': 'cpu_intel_platinum_8260'}}
          #self.extra_resources = {'constraint': {'type': 'v100'}}
          #self.extra_resources = {'memory': {'size': '700G'}}
      
          self.time_limit= '2h'
          self.prerun_cmds= ['module purge','module load gpustack','module load dl','module load cuda/10.2.89',
                             'module load pytorch/1.5.1 torchvision horovod/0.19.2',
                             'module swap openmpi-gpu openmpi/4.0.3-cuda10.2',
                             'export OMPI_MCA_btl_openib_warn_no_device_params_found=0',
                             'export UCX_MEMTYPE_CACHE=n','export UCX_TLS=tcp',
                             'export DATA_DIR="/local/reference/CV/ILSVR/classification-localization/data/jpeg"',
                             'export main_exe="./pytorch_imagenet_resnet50_less_val_revised.py"','batch_size=256',
                             'epochs=1','module list']
          self.executable= 'time -p srun -u --cpu-bind=cores python3 ${main_exe} --epochs ${epochs} --batch-size ${batch_size} --train-dir ${DATA_DIR}/train --val-dir ${DATA_DIR}/val'

          if self.variant == 'v100_8_multinode':
             
             self.extra_resources = {'constraint': {'type': 'v100,cpu_intel_platinum_8260'}}
             self.extra_resources = {'memory': {'size': '700G'}}
             self.num_tasks= 16
             self.num_cpus_per_task=6

          elif self.variant == 'v100_8_singlenode':
             self.extra_resources = {'constraint': {'type': 'v100,cpu_intel_platinum_8260'}}
             self.extra_resources = {'memory': {'size': '700G'}}
             self.num_tasks=8
             self.num_cpus_per_task=4

          elif self.variant == 'a100_4_singlenode':
             self.extra_resources = {'constraint': {'type': 'a100,4gpus'}}
             self.extra_resources = {'memory': {'size': '450G'}}
             self.num_tasks=4
             self.num_cpus_per_task=14
             

          elif self.variant == 'a100_8_singlenode':
             self.extra_resources = {'constraint': {'type': 'a100,8gpus'}}
             self.extra_resources = {'memory': {'size': '450'}}
             self.num_tasks=8
             self.num_cpus_per_task=5




      @rfm.run_before('run')
      def set_job_options(self):
        if self.variant== 'v100_8_multinode':
           self.job.options = ['--gpus=16',
                              '--gpus-per-node=4',
                              '--constraint=v100,cpu_intel_platinum_8260',
                              '--account=ibex-cs',
                              '--output=rfm_pytorch_v100_8_multinode_job.err',  
                              '--error=rfm_pytorch_v100_8_multinode_job.out']

        elif self.variant== 'v100_8_singlenode':
           self.job.options = ['--gpus=8',
                              '--gpus-per-node=8',
                              '--constraint=v100',
                              '--account=ibex-cs',
                              '--output=rfm_pytorch_v100_8_singlenode_job.err',
                              '--error=rfm_pytorch_v100_8_singlenode_job.out']

        elif self.variant== 'a100_8_singlenode':
           self.job.options = ['--gpus=8',
                              '--gpus-per-node=8',
                              '--account=ibex-cs',
                              '--output=rfm_pytorch_job.err',
                              '--error=rfm_pytorch_job.out']

        elif self.variant== 'a100_4_singlenode':
           self.job.options = ['--gpus=4',
                              '--constraint=a100,4gpus',
                              '--gpus-per-node=4',
                              #'--account=ibex-cs',
                              '--output=rfm_pytorch_job.err',
                              '--error=rfm_pytorch_job.out']



      @rfm.run_before('sanity')
      def set_sanity_patterns(self):
          self.sanity_patterns = sn.assert_found(r'real', self.stdout)

         


      @rfm.run_before('performance')
      def set_perf_patterns(self):
          self.perf_patterns = {'real': sn.extractsingle(r'real\s(\S+)\s+',self.stdout, 1, float)}

      # Refrerence according to running training on 16 gpus and can be revised
      reference = {
                        'ibex' : {
                                'real' : (300,None,+10,None),

                        }
                }
