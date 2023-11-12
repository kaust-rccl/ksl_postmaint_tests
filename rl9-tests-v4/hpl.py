import os
import reframe as rfm
import reframe.utility.sanity as sn

class hpl_test(rfm.RunOnlyRegressionTest):
      maintainers = ['rana.selim@kaust.edu.sa']
      descr = 'running hpl tests for v100 and a100'
    #  tags = {'hpl','gpu','acceptance'}
    #  sourcesdir= '../src/hpl/'
      path='HPL.out'
    #  valid_prog_environs = ['gpustack_builtin']
    #  time_limit = "1h"
                
                
@rfm.simple_test
class hpl_cpu(hpl_test):
      variant = parameter(['intel','amd'])
      valid_systems = ['ibex:batch']
      tags= { 'hpl','cpu'}
      reference = {
                        'ibex' : {
                               'amd' : (2600,-0.06,None,'Gflops'),
                               'intel' : (1800,-0.06,None,'Gflops')
                        }
                }       
      
      @run_after('init')
      def setting_variables(self):
       if  self.variant == 'intel':
        self.valid_systems = ['ibex:batch']
        self.valid_prog_environs = ['cpustack_builtin']
        self.time_limit='10m'
        self.sourcesdir='../src/hpl/cpu/intel'

        self.modules=['openmpi/4.1.4/intel2022.3']
        self.num_tasks=1
        self.num_tasks_per_node=1
        self.num_cpus_per_task=40
        self.prerun_cmds = ['./env.sh']
        self.executable = ' srun -c ${SLURM_CPUS_PER_TASK} ./xhpl'
        self.extra_resources = {'constraint': {'type': 'intel'},'nodes': {'num_of_nodes': '1'}}
        self.tags |= {'intel'}
       elif  self.variant == 'amd':
        self.valid_systems = ['ibex:batch']
        self.valid_prog_environs = ['cpustack_builtin']
        self.time_limit='10m'
        self.sourcesdir='../src/hpl/cpu/amd'
        self.modules=['mpich/4.0.3/intel2022.3','openmpi/4.1.4/gnu11.2.1']
        self.num_tasks=128
        self.num_tasks_per_node=128
        self.num_cpus_per_task=1
        self.prerun_cmds = ['./env.sh']
        self.executable = 'mpirun -np 128 -mca ucx -x ./xhpl'
        self.extra_resources = {'memory': {'size': '450G'},'constraint': {'type': 'amd'},'nodes': {'num_of_nodes': '1'}}
        self.tags |= {'amd'}




      @run_before('sanity')
      def set_sanity_patterns(self):
          self.sanity_patterns = sn.all([
            sn.assert_found('End of Tests.', self.stdout),
            sn.assert_found('0 tests completed and failed residual checks', self.stdout),
            sn.assert_found('0 tests skipped because of illegal input values.', self.stdout)
        ])


      @run_before('performance')
      def set_perf_patterns(self):
          self.perf_patterns = {self.variant : sn.extractsingle(r'^W[R|C]\S+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d[\d.]+\s+(?P<Gflops>\d[\d.eE+]+)', self.stdout, 'Gflops', float)}
                                                             
     
@rfm.simple_test
class hpl_gpu(hpl_test):
      variant = parameter(['p100','v100_4','v100_8','a100_4','a100_8'])
      valid_systems = ['ibex:gpu']
      valid_prog_environs = ['gpustack_builtin']
      tags= { 'hpl','gpu'}
      sourcesdir= '../src/hpl/gpu'
      time_limit='30m'

   
   

      reference = {
                        'ibex' : {
                               'p100' : (47000,-0.05,None,'Gflops'),
                               'v100_8' : (35600,-0.05,None,'Gflops'),
                               'v100_4' : (52000,-0.05,None,'Gflops'),
                               'a100_4' : (47000,-0.05,None,'Gflops'),
                               'a100_8' : (47000,-0.05,None,'Gflops'),




                        }
                }
      
      @run_after('init')
      def setting_variables(self):
        if  self.variant == 'p100':
           self.num_tasks=4
           self.executable='srun -u -n ${SLURM_NTASKS} -c ${CPUS} --cpu-bind=none singularity run --nv $IMAGE hpl.sh --cpu-affinity +0-15:0-15:18-33:18-33 --cpu-cores-per-rank ${CPUS} --gpu-affinity 0:1:2:3 --dat ./HPL.dat.p100'
           self.num_cpus_per_task=8
           self.extra_resources = {'memory': {'size': '240G'},'constraint': {'type': 'p100'}}

           self.prerun_cmds = ['module purge','module load gpustack','module load singularity','module load openmpi/4.0.3-cuda11.2.2','export IMAGE=./hpl_sing.sif','export CPUS=8','export HPL=./HPL.out', 'echo hostname > HPL.out','./env.sh']


        elif self.variant == 'v100_8': 
           self.num_tasks=8
          # self.executable='--bind-to none --nooversubscribe singularity run --nv $IMAGE hpl.sh --cpu-cores-per-rank ${CPUS} \
#--cpu-affinity 2-5:6-9:10-13:14-17:24-27:28-31:32-37:38-41 \
#--gpu-affinity 0:1:2:3:4:5:6:7 --dat  ./HPL.dat.v100.G8N1'
           self.executable='srun -u -n ${SLURM_NTASKS} -c ${CPUS} --cpu-bind=none singularity run --nv $IMAGE hpl.sh --cpu-affinity 3-7:7-11:11-15:15-19:24-28:28-32:32-36:36-40 --cpu-cores-per-rank ${CPUS} --gpu-affinity 0:1:2:3:4:5:6:7  --dat ./HPL.dat.v100.G8N1'
           self.num_cpus_per_task=5
          # self.num_gpus_per_node=4

           self.extra_resources = {'memory': {'size': '450G'},'constraint': {'type': 'v100,gpu_ai'}}
           
           self.prerun_cmds = ['module purge','module load rl9-gpustack','module load singularity','export IMAGE=./hpl_sing.sif','export CPUS=5','export HPL=./HPL.out', 'echo hostname > HPL.out','./env.sh']
           self.tags |= {'v100_8'}

        elif self.variant == 'v100_4':
           self.num_tasks=4
           self.num_cpus_per_task=7
           self.num_gpus_per_node=4
           self.extra_resources = {'memory': {'size': '340G'},'constraint': {'type': 'cpu_intel_gold_6142'}}
           self.executable='srun -u -n ${SLURM_NTASKS} -c ${CPUS} --cpu-bind=none singularity run --nv $IMAGE hpl.sh --cpu-affinity 3-9:9-15:16-22:22-28 --cpu-cores-per-rank ${CPUS} --gpu-affinity 0:1:2:3 --dat ./HPL.dat.v100.G4N1'
           self.prerun_cmds = ['module purge','module load rl9-gpustack','module load singularity','export IMAGE=./hpl_sing.sif','export CPUS=7','export HPL=./HPL.out', 'echo hostname > HPL.out','./env.sh']
           self.tags |= {'v100_4'}

     
        elif self.variant == 'a100_8':
           self.num_tasks=4
           self.num_gpus_per_node=8
           self.extra_resources = {'memory': {'size': '0'},'constraint': {'type': 'a100,8gpus'},'nodes': {'num_of_nodes': '1'}}
           self.executable='run -u -n ${SLURM_NTASKS} -c ${CPUS} --cpu-bind=none singularity run --nv $IMAGE hpl.sh --cpu-affinity +32-63:32-63:0-31:0-31:96-127:96-127:64-95:64-95 --cpu-cores-per-rank ${CPUS} --gpu-affinity 0:1:2:3:4:5:6:7 --dat ./HPL.dat.a100_8'
           self.num_cpus_per_task=16

           self.prerun_cmds = ['module purge','module load rl9-gpustack','module load singularity','export IMAGE=./hpl_sing.sif','export CPUS=8','export OMPI_MCA_btl_openib_warn_no_device_params_found=0','./env.sh']

        elif self.variant == 'a100_4':
           self.num_tasks=4
           self.num_gpus_per_node=4
           self.extra_resources = {'memory': {'size': '450G'},'constraint': {'type': 'a100,4gpus'},'nodes': {'num_of_nodes': '1'}}
           #self.executable='srun -u -n ${SLURM_NTASKS} -c ${CPUS} --cpu-bind=none singularity run --nv $IMAGE hpl.sh --cpu-affinity +32-63:32-63:0-31:0-31 --cpu-cores-per-rank ${CPUS} --gpu-affinity 0:1:2:3 --dat ./HPL.dat.a100.G4N1'
           self.executable='srun -u -n 4 -c 15 --cpu-bind=sockets,verbose singularity run --nv $IMAGE hpl.sh --cpu-cores-per-rank ${CPUS} --cpu-affinity 5-12:18-25:32-39:52-59 --gpu-affinity 2:3:0:1  --dat ./HPL.dat.a100.G4N1'
           self.num_cpus_per_task=15
           self.tags |= {'a100_4'}


           self.prerun_cmds = ['module purge','module load rl9-gpustack','module load singularity','module load openmpi/4.1.4/intel2022.3_cuda11.8','export IMAGE=./hpl_sing.sif','export CPUS=4','export OMPI_MCA_btl_openib_warn_no_device_params_found=0','./env.sh']

      @run_before('run')
      def set_job_options(self):
        if self.variant== 'v100_8':
           self.job.options = ['--partition=batch','--gpus=8','--gpus-per-node=8']
        elif self.variant== 'a100_4' or self.variant=='v100_4' :
           self.job.options = ['--partition=batch']



      @run_before('sanity')

      def set_sanity_patterns(self):
           self.sanity_patterns = sn.all([
            sn.assert_found('End of Tests.', self.path),
            sn.assert_found('0 tests completed and failed residual checks', self.path),
            sn.assert_found('0 tests skipped because of illegal input values.', self.path)
        ])

 
      @run_before('performance')
      def set_perf_patterns(self):
           self.perf_patterns = {self.variant : sn.extractsingle(r'^W[R|C]\S+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d[\d.]+\s+(?P<Gflops>\d[\d.eE+]+)', self.path, 'Gflops', float)}
          
