# An example of system check where the mpi launcher is omitted in the jobscript.
import reframe as rfm
import reframe.utility.sanity as sn
import os
class system_check(rfm.RunOnlyRegressionTest):
      variant= parameter(['homefs','scartchfs','aifs','userfs','projectfs','localfs','lustrefs','lustrefs2','modulepath','numanodes','ibvdev','os','kernal'])
      maintainers = ['rana.selim@kaust.edu.sa']
      descr = 'System sanity check on ibex nodes'
      tags = {'fs','acceptance'}
      sourcesdir= None
      time_limit = "10m"

@rfm.simple_test
class system_cpu(system_check):
#      variant= parameter(['home','wekaio'])
#      params = parameter(['cpu','gpu'])
       
     # descr = 'Filesystem mount check on longin and compute nodes'
      valid_systems = ['ibex:login','ibex:batch']
      valid_prog_environs = ['cpustack_builtin']
      sourcesdir=None
      executable='mount'
      time_limit='10m'
      tags = {'system','acceptance','cpu','fs','sys'}

      @run_after('init')
      def setting_parameters(self):
       if self.variant == "homefs":
         self.sanity_patterns =sn.assert_found(r'/home/home',self.stdout)
       elif self.variant == "scratchfs":
         self.sanity_patterns =sn.assert_found(r'/ibex/scratch',self.stdout)
       elif  self.variant == "aifs":  
         self.sanity_patterns =sn.assert_found(r'/ibex/ai',self.stdout)
       elif  self.variant == "userfs":
         self.sanity_patterns =sn.assert_found(r'/ibex/user',self.stdout)
       elif  self.variant == "projectfs":
         self.sanity_patterns =sn.assert_found(r'/ibex/project',self.stdout)
       elif  self.variant == "localfs":
         self.sanity_patterns =sn.assert_found(r'/local',self.stdout)
       elif  self.variant == "lustrefs":
         self.sanity_patterns =sn.assert_found(r'/lustre',self.stdout)
       elif  self.variant == "lustrefs2":
         self.sanity_patterns =sn.assert_found(r'/lustre2',self.stdout)
       elif  self.variant == "modulepath":
         self.executable='echo $MODULEPATH'
         self.sanity_patterns =sn.assert_found(r'/sw/rl9c/modulefiles/applications:/sw/rl9c/modulefiles/compilers:/sw/rl9c/modulefiles/libs:/sw/services_rl9/modulefiles',self.stdout)
       elif  self.variant == "numanodes":
         self.executable='numactl -H'
         self.sanity_patterns =sn.assert_found(r'2 nodes',self.stdout)
       elif  self.variant == "ibvdev":
         self.executable='ibv_devinfo -l'
         self.sanity_patterns =sn.assert_found(r'mlx5_0',self.stdout)
       elif  self.variant == "os":
         self.executable='cat /etc/redhat-release'
         self.sanity_patterns =sn.assert_found(r'Rocky Linux release 9.1',self.stdout)
       elif  self.variant == "kernal":
         self.executable='uname -r '
         self.sanity_patterns =sn.assert_found(r'5.14.0-162.23.1.el9_1.x86_64',self.stdout)



@rfm.simple_test
class system_gpu(system_check):
      variant= parameter(['homefs','scartchfs','aifs','userfs','projectfs','localfs','lustrefs','lustrefs2','modulepath','numanodes','ibvdev','nvidiasmi','devicequery','os','kernal'])

      descr = 'System sanity check on gpu nodes'
      valid_systems = ['ibex:gpu','ibex:gpu24','ibex:gpu_wide24']
      valid_prog_environs = ['gpustack_builtin']
      num_gpus_per_node=1
      num_tasks=1
      sourcesdir=None
      executable='mount'
      time_limit='10m'
      tags = {'fs','acceptance','gpu','system','sys'}

      @run_after('init')
      def setting_parameters(self):
       if self.variant == "homefs":
         self.sanity_patterns =sn.assert_found(r'/home/home',self.stdout)
       elif self.variant == "scratchfs":
         self.sanity_patterns =sn.assert_found(r'/ibex/scratch',self.stdout)
       elif  self.variant == "aifs":
         self.sanity_patterns =sn.assert_found(r'/ibex/ai',self.stdout)
       elif  self.variant == "userfs":
         self.sanity_patterns =sn.assert_found(r'/ibex/user',self.stdout)
       elif  self.variant == "projectfs":
         self.sanity_patterns =sn.assert_found(r'/ibex/project',self.stdout)
       elif  self.variant == "localfs":
         self.sanity_patterns =sn.assert_found(r'/local',self.stdout)
       elif  self.variant == "lustrefs":
         self.sanity_patterns =sn.assert_found(r'/lustre',self.stdout)
       elif  self.variant == "lustrefs2":
         self.sanity_patterns =sn.assert_found(r'/lustre2',self.stdout)
       elif  self.variant == "modulepath":
         self.executable='echo $MODULEPATH'
         self.sanity_patterns =sn.assert_found(r'/sw/rl9g/modulefiles/libs:/sw/rl9g/modulefiles/compilers:/sw/rl9g/modulefiles/applications:/sw/services_rl9/modulefiles',self.stdout)
       elif  self.variant == "nvidiasmi":
         self.executable='nvidia-smi'
         self.sanity_patterns =sn.assert_found(r'NVIDIA-SMI',self.stdout)
       elif  self.variant == "numanodes":
         self.executable='numactl -H'
         self.sanity_patterns =sn.assert_found(r' 2 nodes',self.stdout)
       elif  self.variant == "ibvdev":
         self.executable='ibv_devinfo -l'
         self.sanity_patterns =sn.assert_found(r'mlx5_0',self.stdout)
       elif  self.variant == 'devicequery':
         self.executable='./deviceQuery'
         self.sourcesdir='../src/devicequery'
         self.sanity_patterns =sn.assert_found(r'Result = PASS',self.stdout)
       elif  self.variant == "os":
         self.executable='cat /etc/redhat-release'
         self.sanity_patterns =sn.assert_found(r'Rocky Linux release 9.1',self.stdout)
       elif  self.variant == "kernal":
         self.executable='uname -r '
         self.sanity_patterns =sn.assert_found(r'5.14.0-162.23.1.el9_1.x86_64',self.stdout)


      @run_before('run')
      def set_job_options(self):
         self.job.options = ['--partition=batch','--gpus=1','--gpus-per-node=1']
 
      #maintainers = ['rana.selim@kaust.edu.sa']
      #tags = {'filesystem','acceptance','cpu','fs'}

































