import os
import reframe as rfm
import reframe.utility.sanity as sn

class osu_test(rfm.RunOnlyRegressionTest):
      variant= parameter(['latency', 'bandwidth','bibandwidth'])
      maintainers = ['mohsin.shaikh@kaust.edu.sa']
      descr = 'running OSU BM'
      #tags = {'osu','acceptance'}
      sourcesdir= None
      time_limit = "10m"



@rfm.simple_test
class osu_gpu_v100(osu_test):
      params = parameter(['v100&cpu_intel_gold_6142','v100&gpu_ai'])
      valid_prog_environs = ['gpustack_builtin']
      valid_systems = ['ibex:batch']
      modules = ['openmpi/4.1.4/gnu11.2.1-cuda11.8']
      tags = {'gpu','osu','acceptance'}
      num_tasks = 2
      num_tasks_per_node = 1
      sourcesdir = '../src/env'



      @run_before('run')
      def set_job_options(self):
          self.job.options = ['--constraint="%s"'%(self.params),
                              '--gpus=2',
                              '--gpus-per-node=1']
      @run_after('init')
      def setting_parameters(self):
        if 'v100' in self.params:
            self.tags |= {'v100'}

        if self.variant == "latency":
           self.prerun_cmds = ['./env.sh']
           self.executable='nvidia-smi --query-gpu=gpu_name,gpu_bus_id --format=csv;srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} ${OSU_DIR}/get_local_rank osu_latency H H'
           self.sanity_patterns = sn.assert_found(r'^# OSU MPI-CUDA ', self.stdout)
           self.perf_patterns = {
                                self.variant: sn.extractsingle(r'^4194304\s+(?P<FourGBlat>\S+)',self.stdout, 'FourGBlat', float)}


        elif self.variant == "bandwidth":
           self.prerun_cmds = ['./env.sh']
           self.executable='nvidia-smi --query-gpu=gpu_name,gpu_bus_id --format=csv;srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} ${OSU_DIR}/get_local_rank osu_bw H H'
           self.sanity_patterns = sn.assert_found(r'^# OSU MPI-CUDA ', self.stdout)
           self.perf_patterns = {self.variant: sn.extractsingle(r'^4194304\s+(?P<FourGBbw>\S+)',self.stdout, 'FourGBbw', float)}

        elif self.variant == "bibandwidth":
           self.prerun_cmds = ['./env.sh']
           self.executable= 'nvidia-smi --query-gpu=gpu_name,gpu_bus_id --format=csv;srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} ${OSU_DIR}/get_local_rank osu_bibw H H'
           self.sanity_patterns = sn.assert_found(r'^# OSU MPI-CUDA ', self.stdout)
           self.perf_patterns = {self.variant: sn.extractsingle(r'^4194304\s+(?P<FourGBbibw>\S+)',self.stdout, 'FourGBbibw', float)}

      reference = {
                        'ibex' : {
                                'latency' : (160.0,None,0.1,None),
                                'bandwidth' : (305000.0,-0.1,None,None),
                                'bibandwidth' : (270000.0,-0.1,None,None),
                                 }
                        }
                        
                        
@rfm.simple_test
class osu_gpu(osu_test):
      params = parameter(['p100', 'rtx2080ti', 'gtx1080ti'])
      valid_prog_environs = ['gpustack_builtin']
      valid_systems = ['ibex:batch']
      modules = ['openmpi/4.1.4/gnu11.2.1-cuda11.8']
      tags = {'gpu','osu','acceptance'}
      num_tasks = 2
      num_tasks_per_node = 1
      sourcesdir = '../src/env'



      @run_before('run')
      def set_job_options(self):
          self.job.options = ['--constraint="%s"'%(self.params),
                              '--gpus=2',
                              '--gpus-per-node=1']
      @run_after('init')
      def setting_parameters(self):
        if 'p100' in self.params:
            self.tags |= {'p100'}
        if 'rtx2080ti' in self.params:
            self.tags |= {'rtx2080ti'}
        if 'gtx1080ti' in self.params:
            self.tags |= {'gtx1080ti'}

        if self.variant == "latency":
           self.prerun_cmds = ['./env.sh']
           self.executable='nvidia-smi --query-gpu=gpu_name,gpu_bus_id --format=csv;srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} ${OSU_DIR}/get_local_rank osu_latency H H'
           self.sanity_patterns = sn.assert_found(r'^# OSU MPI-CUDA ', self.stdout)
           self.perf_patterns = {
                                self.variant: sn.extractsingle(r'^4194304\s+(?P<FourGBlat>\S+)',self.stdout, 'FourGBlat', float)}


        elif self.variant == "bandwidth":
           self.prerun_cmds = ['./env.sh']
           self.executable='nvidia-smi --query-gpu=gpu_name,gpu_bus_id --format=csv;srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} ${OSU_DIR}/get_local_rank osu_bw H H'
           self.sanity_patterns = sn.assert_found(r'^# OSU MPI-CUDA ', self.stdout)
           self.perf_patterns = {self.variant: sn.extractsingle(r'^4194304\s+(?P<FourGBbw>\S+)',self.stdout, 'FourGBbw', float)}

        elif self.variant == "bibandwidth":
           self.prerun_cmds = ['./env.sh']
           self.executable= 'nvidia-smi --query-gpu=gpu_name,gpu_bus_id --format=csv;srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} ${OSU_DIR}/get_local_rank osu_bibw H H'
           self.sanity_patterns = sn.assert_found(r'^# OSU MPI-CUDA ', self.stdout)
           self.perf_patterns = {self.variant: sn.extractsingle(r'^4194304\s+(?P<FourGBbibw>\S+)',self.stdout, 'FourGBbibw', float)}

      reference = {
                        'ibex' : {
                                'latency' : (650.0,None,0.1,None),
                                'bandwidth' : (6500.0,-0.1,None,None),
                                'bibandwidth' : (12500.0,-0.1,None,None),
                                 }
                        }

@rfm.simple_test
class osu_cpu(osu_test):
      valid_prog_environs = ['cpustack_gnu']
      valid_systems = ['ibex:batch_mpi']
      num_tasks = 2
      num_tasks_per_node = 1
      modules = ['openmpi/4.1.4/gnu11.2.1']
      sourcesdir = '../src/env'
      tags = {'cpu','osu','acceptance'}
      @run_after('init')
      def setting_parameters(self):
        if self.variant == "latency":
           self.prerun_cmds = ['./env.sh']
           self.executable='osu_latency'
           self.sanity_patterns = sn.assert_found(r'# OSU MPI Latency Test v5.9', self.stdout)
           self.perf_patterns = {
                                self.variant: sn.extractsingle(r'^4194304\s+(?P<FourGBlat>\S+)',self.stdout, 'FourGBlat' , float)}


        elif self.variant == "bandwidth":
           self.prerun_cmds = ['./env.sh']
           self.executable='osu_bw'
           self.sanity_patterns = sn.assert_found(r'^# OSU MPI Bandwidth Test v5.9', self.stdout)
           self.perf_patterns = {self.variant: sn.extractsingle(r'^4194304\s+(?P<FourGBbw>\S+)',self.stdout, 'FourGBbw', float)}

        elif self.variant == "bibandwidth":
           self.prerun_cmds = ['./env.sh']
           self.executable= 'osu_bibw'
           self.sanity_patterns = sn.assert_found(r'^# OSU MPI Bi-Directional Bandwidth Test v5.9', self.stdout)
           self.perf_patterns = {self.variant: sn.extractsingle(r'^4194304\s+(?P<FourGBbibw>\S+)',self.stdout, 'FourGBbibw', float)}

      reference = {
                        'ibex' : {
                                'latency' : (390.0,None,0.1,'FourGBlat'),
                                'bandwidth' : (12000.0,-0.1,None,'FourGBbw'),
                                'bibandwidth' : (24000.0,-0.1,None,'FourGBbibw'),
                                 }
                        }
