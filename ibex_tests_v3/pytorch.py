import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class pytorch_test(rfm.RunOnlyRegressionTest):



           ## TEST BASIC INFO
      maintainers = ['rana.selim@kaust.edu.sa']
      descr = 'running pytorch test'
      tags = {'pytorch'}

           ## SETTING TEST ENV
      sourcesdir= None
      valid_prog_environs = ['gpustack_builtin']
      valid_systems = ['ibex:batch']
      modules = ['dl','cuda/10.2.89','pytorch/1.5.1','torchvision','horovod/0.19.2']
     
      @rfm.run_after('init')
      def setting_variables(self):

          self.num_tasks= 8
          self.num_cpus_per_task=6
          self.extra_resources = {'constraint': {'type': 'v100'}}
          self.extra_resources = {'memory': {'size': '256G'}}
      
          self.time_limit= '2h'
          self.prerun_cmds= ['module swap openmpi-gpu openmpi/4.0.3-cuda10.2','export OMPI_MCA_btl_openib_warn_no_device_params_found=0','export UCX_MEMTYPE_CACHE=n','export UCX_TLS=tcp','export DATA_DIR="/local/reference/CV/ILSVR/classification-localization/data/jpeg"','export main_exe="/opt/pytorch_imagenet_resnet50_less_val_revised.py"','batch_size=256','epochs=1','module list']
          self.executables= ['time -p srun -u --cpu-bind=cores python3 ${main_exe} --epochs ${epochs} --batch-size ${batch_size} --train-dir ${DATA_DIR}/train --val-dir ${DATA_DIR}/val"']

      




             

      
    


      @rfm.run_before('run')
      def set_job_options(self):
          self.job.options = ['--gpus=32','--gpus-per-node=8','--account=ibex_cs']


      @rfm.run_before('sanity')
      def set_sanity_patterns(self):
          self.sanity_patterns = sn.assert_found(r'real', self.stdout)
         


       
