import os
import reframe as rfm
import reframe.utility.sanity as sn

class osu_test(rfm.RunOnlyRegressionTest):
      variant= parameter(['latency', 'bandwidth','bibandwidth'])
      maintainers = ['rana.selim@kaust.edu.sa']
      descr = 'running OSU BM'
      tags = {'osu','acceptance','a100'}
      sourcesdir= None
      time_limit = "10m"



@rfm.simple_test
class osu_a100(osu_test):

      params= parameter(['a100&4gpus', 'a100&8gpus'])

           ## TEST BASIC INFO
      maintainers = ['rana.selim@kaust.edu.sa']
      descr = 'running osu  tests'


           ## SETTING TEST ENV
      sourcesdir= '../src/env'
      valid_prog_environs = ['gpustack_builtin']
      valid_systems = ['ibex:batch']
      modules = ['openmpi/4.1.4/gnu11.2.1-cuda11.8']

      
          ## RUN AND VALIDATE
      @run_after('init')
      def setting_variables(self):

           self.num_tasks=2
           self.num_tasks_per_node=1
           self.time_limit = '10m'
           #self.extra_resources = {'constraint': {'type': 'a100,4gpus'}}
           self.num_cpus_per_task=62
           self.tags = {'gpu','osu',self.variant}

      @run_before('run')
      def set_job_options(self):
          self.job.options = ['--constraint="%s"'%(self.params),
                              '--gpus=8',
                              '--gpus-per-node=4']
      @run_after('init')
      def setting_parameters(self):
         if 'v100' in self.params:
            self.tags |= {'v100'}
         elif 'a100' in self.params:
            self.tags |= {'a100'}

            if '4gpus' in self.params:
               self.tags |= {'4gpus'}

            elif '8gpus' in self.params:
               self.tags |= {'8gpus'}
 
      
         if self.variant == "latency":
            self.prerun_cmds = ['./env.sh']
            self.executable='srun -n 2 -N 2 --cpu-bind=cores $OSU_DIR/get_local_rank osu_latency -m 4194304:4194304 -d cuda -x 100 -i 100 D D'
            self.sanity_patterns = sn.assert_found(r'^# OSU MPI-CUDA ', self.stdout)
            self.perf_patterns = {
                                self.variant: sn.extractsingle(r'^4194304\s+(?P<FourGBlat>\S+)',self.stdout, 'FourGBlat', float)}


         elif self.variant == "bandwidth":
            self.prerun_cmds = ['./env.sh']
            self.executable='srun -n 2 -N 2 --cpu-bind=cores $OSU_DIR/get_local_rank osu_bw -m 4194304:4194304 -d cuda -x 100 -i 100 D D'

            self.sanity_patterns = sn.assert_found(r'^# OSU MPI-CUDA ', self.stdout)
            self.perf_patterns = {self.variant: sn.extractsingle(r'^4194304\s+(?P<FourGBbw>\S+)',self.stdout, 'FourGBbw', float)}

         elif self.variant == "bibandwidth":
            self.prerun_cmds = ['./env.sh']
            self.executable='srun -n 2 -N 2 --cpu-bind=cores  $OSU_DIR/get_local_rank osu_bibw -m 4194304:4194304 -d cuda -x 100 -i 100 D D'
            self.sanity_patterns = sn.assert_found(r'^# OSU MPI-CUDA ', self.stdout)
            self.perf_patterns = {self.variant: sn.extractsingle(r'^4194304\s+(?P<FourGBbibw>\S+)',self.stdout, 'FourGBbibw', float)}


      reference = {
                        'ibex' : {
                                'latency' : (180.0,None,0.1,None),
                                'bandwidth' : (24200.0,-0.1,None,None),
                                'bibandwidth' : (36100.0,-0.1,None,None),
                                 }
                        }
