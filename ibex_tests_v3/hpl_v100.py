import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class hpl_tests(rfm.RunOnlyRegressionTest):

      variant= parameter(['v100_8_singlenode'])

           ## TEST BASIC INFO
      maintainers = ['rana.selim@kaust.edu.sa']
      descr = 'running hpl tests'
      path = variable(str)
           ## SETTING TEST ENV
      sourcesdir= None
      valid_prog_environs = ['gpustack_builtin']
      valid_systems = ['ibex:batch_mpi']
      reference = {
                        'ibex' : {
                               'v100_8_singlenode' : (47000,-0.05,None,'Gflops')

                        }
                }
      
          ## RUN AND VALIDATE
      @rfm.run_after('init')
      def setting_variables(self):
        self.path='HPL.out'
        if self.variant == 'v100_8_singlenode': 
           self.time_limit = '1h'
           self.num_tasks=8
           self.executable='--bind-to none --nooversubscribe singularity run --nv $IMAGE hpl.sh --cpu-cores-per-rank ${CPUS} \
--cpu-affinity 2-5:6-9:10-13:14-17:24-27:28-31:32-37:38-41 \
--gpu-affinity 0:1:2:3:4:5:6:7 --dat  ./HPL.dat.v100.G8N1'
           self.num_cpus_per_task=5
           self.extra_resources = {'memory': {'size': '450G'},'constraint': {'type': 'v100,gpu_ai'}}
           
           self.prerun_cmds = ['module purge','module load gpustack','module load singularity','module load openmpi/4.0.3-cuda11.2.2','export IMAGE=./hpl_sing.sif','export CPUS=4','export HPL=./HPL.out', 'echo hostname > HPL.out']

           self.sourcesdir='../src/hpl/'
        self.tags = {'hpl','gpu',self.variant,'acceptance'}

                
    


      @rfm.run_before('run')
      def set_job_options(self):
        if self.variant== 'v100_8_singlenode':
           self.job.options = ['--gpus=8','--gpus-per-node=8']



      @rfm.run_before('sanity')

      def set_sanity_patterns(self):
          self.sanity_patterns = sn.all([
            sn.assert_found('End of Tests.', self.path),
            sn.assert_found('0 tests completed and failed residual checks', self.path),
            sn.assert_found('0 tests skipped because of illegal input values.', self.path)
        ])

 
      @rfm.run_before('performance')
      def set_perf_patterns(self):
          self.perf_patterns = {self.variant : sn.extractsingle(r'^W[R|C]\S+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d[\d.]+\s+(?P<Gflops>\d[\d.eE+]+)', self.path, 'Gflops', float)}

