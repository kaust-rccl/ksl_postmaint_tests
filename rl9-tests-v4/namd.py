import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class namd_check(rfm.RunOnlyRegressionTest):
      variant= parameter(['v100_8', 'a100_8'])

      @run_after('init')
      def setting_variables(self):

        self.descr = 'NAMD 2.13 CUDA version benchmark apoa1'
        
        self.valid_systems = ['ibex:batch'] 
   
        self.valid_prog_environs = ['gpustack_builtin']
        
        self.sourcesdir='../src/namd'
        
        
        self.modules=['namd']
        #/2.13/cuda10-verbs-smp-icc17
        self.prerun_cmds = ['module list','which namd2','hostname','echo $MODULEPATH']
        #['export SLURM_CPU_BIND_TYPE=sockets','export SLURM_CPU_BIND_VERBOSE=verbose']
 
        self.executable='namd2'
        self.executable_opts = '+p8 +devices 0,1,2,3,4,5,6,7 +idlepoll  apoa1.namd'.split()
        
        
        # Job script attributes

        self.time_limit = '1h'
        self.num_tasks = 1
        self.num_tasks_per_node = 1
        self.num_gpus_per_node=8
        self.num_cpus_per_task=8
        if self.variant == 'v100_8' :
           self.extra_resources = {'constraint': {'type': 'v100,gpu_ai'}}
        elif self.variant == 'a100_8' :
           self.extra_resources = {'constraint': {'type': 'a100,8gpus'}}
           self.tags = { 'a100'}
        self.sanity_patterns = sn.assert_eq(sn.count(sn.extractall(r'TIMING: (?P<step_num>\S+)  CPU:', self.stdout, 'step_num')),25)
        
        self.perf_patterns = {       
                    'days_ns': sn.avg(sn.extractall('Info: Benchmark time: \S+ CPUs \S+ ''s/step (?P<days_ns>\S+) days/ns \S+ MB memory', self.stdout, 'days_ns', float))
                               }
        
  
        self.reference = {
                            'ibex' : {      'days_ns': (0.037, None, 0.1,'days_ns')
                                            },
                            }
        
        self.tags = {'namd','gpu',self.variant,'acceptance'}

        
        # initials or email of the maintainer    
        self.maintainers = ['MS']

   # def setup(self,partition,environ,**job_opts):
       # super().setup(partition,environ,**job_opts)
        #self.job.options = [ '--gres=gpu:%s:%s' % ('v100',self.num_gpus_per_node)]
