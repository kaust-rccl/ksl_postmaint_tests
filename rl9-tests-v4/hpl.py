import os
import reframe as rfm
import reframe.utility.sanity as sn

class hpl_test(rfm.RunOnlyRegressionTest):
      maintainers = ['mohamed.elgharawy@kaust.edu.sa']
      descr = 'running hpl tests for cpu/gpu'
    #  tags = {'hpl','gpu','acceptance'}
    #  sourcesdir= '../src/hpl/'
      path='HPL.out'
    #  valid_prog_environs = ['gpustack_builtin']
    #  time_limit = "1h"
                
                
@rfm.simple_test
class hpl_cpu(hpl_test):
      variant = parameter(['intel','amd'])
      valid_systems = ['ibex:batch']
      tags= { 'hpl','cpu','singlenode','acceptance'}
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
      variant = parameter(['p100','v100_4','v100_8','a100_4','a100_8','rtx4090_singlegpu'])
      valid_systems = ['ibex:batch']
      valid_prog_environs = ['gpustack_builtin']
      tags= { 'hpl','gpu','singlenode','acceptance'}
      sourcesdir= '../src/hpl/gpu'
      time_limit='10m'

   
   

      reference = {
                        'ibex' : {
                               'p100' : (1350,-0.05,None,'Gflops'),
                               'v100_8' : (35600,-0.05,None,'Gflops'),
                               'v100_4' : (16500,-0.05,None,'Gflops'),
                               'a100_4' : (56000,-0.05,None,'Gflops'),
                               'a100_8' : (92500,-0.05,None,'Gflops'),
                               'rtx4090_singlegpu' : (1220,-0.05,None,'Gflops')




                        }
                }
      
      @run_after('init')
      def setting_variables(self):
        if  self.variant == 'p100':
           self.num_tasks=4
           self.executable='srun -u -n ${SLURM_NTASKS} -c ${SLURM_CPUS_PER_TASK} --cpu-bind=none singularity run --nv $IMAGE hpl.sh --cpu-affinity 0,3-7:8-13:20-25:26-31  --cpu-cores-per-rank ${CPUS} --gpu-affinity 0:1:2:3 --dat ./HPL.dat.p100'
           self.num_cpus_per_task=8
           self.num_gpus_per_node=4
           self.extra_resources = {'memory': {'size': '230G'},'constraint': {'type': 'p100'}}

           self.prerun_cmds = ['module purge','module load rl9-gpustack','module load singularity','export IMAGE=./hpl_sing.sif','export CPUS=6','export HPL=./HPL.out', 'echo hostname > HPL.out','./env.sh']
           self.tags |= {'p100'}

        elif  self.variant == 'rtx4090_singlegpu':
           self.num_tasks=1
           self.executable='srun -u -n ${SLURM_NTASKS} -c ${SLURM_CPUS_PER_TASK} --cpu-bind=none singularity run --nv $IMAGE hpl.sh --cpu-affinity 0,3-7  --cpu-cores-per-rank ${CPUS} --gpu-affinity 0 --dat ./HPL.dat.4090'
           self.num_cpus_per_task=8
           self.num_gpus_per_node=1
           self.extra_resources = {'memory': {'size': '220G'},'constraint': {'type': 'gpu_rtx4090'}}

           self.prerun_cmds = ['module purge','module load rl9-gpustack','module load singularity','export IMAGE=./hpl_sing.sif','export CPUS=6','export HPL=./HPL.out', 'echo hostname > HPL.out','./env.sh']
           self.tags |= {'rtx4090'}
           self.tags.discard('acceptance')

        elif self.variant == 'v100_8': 
           self.num_tasks=8
           self.executable='srun -u -n ${SLURM_NTASKS} -c ${SLURM_CPUS_PER_TASK} --cpu-bind=none singularity run --nv $IMAGE hpl.sh --cpu-affinity 0,3-5:7-10:12-15:17-20:24-27:28-31:32-35:36-39   --cpu-cores-per-rank ${CPUS} --gpu-affinity 0:1:2:3:4:5:6:7  --dat ./HPL.dat.v100.G8N1'
           self.num_cpus_per_task=5
           self.extra_resources = {'memory': {'size': '450G'},'constraint': {'type': 'v100,gpu_ai'}}
           
           self.prerun_cmds = ['module purge','module load rl9-gpustack','module load singularity',
           'export IMAGE=./hpl_sing.sif',
           'export CPUS=5',
           'export HPL=./HPL.out', 
           'echo hostname > HPL.out','./env.sh']
           self.tags |= {'v100_8'}

        elif self.variant == 'v100_4':
           self.num_tasks=4
           self.num_cpus_per_task=7
           self.num_gpus_per_node=4
           self.extra_resources = {'memory': {'size': '340G'},'constraint': {'type': 'v100,cpu_intel_gold_6142'}}
           self.executable='srun -u -n ${SLURM_NTASKS} -c ${SLURM_CPUS_PER_TASK} --cpu-bind=none singularity run --nv $IMAGE hpl.sh --cpu-affinity 0,3-5:7-10:18-21:23-26 --cpu-cores-per-rank ${CPUS} --gpu-affinity 0:1:2:3 --dat ./HPL.dat.v100.G4N1'
           self.prerun_cmds = ['module purge','module load rl9-gpustack','module load singularity','export IMAGE=./hpl_sing.sif',
           'export CPUS=4',
           'export HPL=./HPL.out', 
           'echo hostname > HPL.out','./env.sh']
           self.tags |= {'v100_4'}

     
        elif self.variant == 'a100_8':
           self.num_tasks=8
           self.num_gpus_per_node=8
           self.extra_resources = {'memory': {'size': '850G'},'constraint': {'type': 'a100,8gpus'},'nodes': {'num_of_nodes': '1'}}
           self.executable='srun -u -n ${SLURM_NTASKS} -c ${SLURM_CPUS_PER_TASK} --cpu-bind=none singularity run --nv $IMAGE hpl.sh --cpu-affinity 30-36:45-51:0,3-7:16-22:90-96:105-111:64-70:75-81 --cpu-cores-per-rank ${CPUS} --gpu-affinity 0:1:2:3:4:5:6:7 --dat ./HPL.dat.a100.G8N1'
           self.num_cpus_per_task=15

           self.prerun_cmds = ['module purge',
           'module load rl9-gpustack',
           'module load singularity',
           'export IMAGE=./hpl_sing.sif',
           'export CPUS=7',
           'export OMPI_MCA_btl_openib_warn_no_device_params_found=0',
           './env.sh']
           self.tags |= {'a100_8'}

        elif self.variant == 'a100_4':
           self.num_tasks=4
           self.num_gpus_per_node=4
           self.extra_resources = {'memory': {'size': '450G'},'constraint': {'type': 'a100,4gpus'},'nodes': {'num_of_nodes': '1'}}
           self.executable='srun -u -n ${SLURM_NTASKS} -c ${SLURM_CPUS_PER_TASK} --cpu-bind=sockets,verbose singularity run --nv $IMAGE hpl.sh --cpu-cores-per-rank ${CPUS} --cpu-affinity 0,3-7:16-22:38-44:52-59 --gpu-affinity 2:3:0:1  --dat ./HPL.dat.a100.G4N1'
           self.num_cpus_per_task=15
           self.tags |= {'a100_4'}


           self.prerun_cmds = ['module purge','module load rl9-gpustack',
           'module load singularity',
           'export IMAGE=./hpl_sing.sif',
           'export CPUS=7',
           'export OMPI_MCA_btl_openib_warn_no_device_params_found=0',
           './env.sh']

      @run_before('run')
      def set_job_options(self):
        if self.variant== 'v100_8'or self.variant== 'a100_8':
           self.job.options = ['--partition=batch','--gpus=8','--gpus-per-node=8']
        elif self.variant== 'a100_4' or self.variant=='v100_4' or self.variant=='p100' :
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
          
