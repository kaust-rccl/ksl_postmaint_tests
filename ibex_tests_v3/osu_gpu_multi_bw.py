import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class osu_test(rfm.RunOnlyRegressionTest):
      variant= parameter(['gpu_multi_bw'])
      maintainers = ['passant.hafez@kaust.edu.sa']
      descr = 'running OSU BM on GPUs'
      tags = {'osu','gpu','bw','bandwidth','acceptance'}
      sourcesdir= None
      valid_systems = ['ibex:batch']
#      valid_prog_environs = ['gpustack_openmpi']
      valid_prog_environs = ['gpustack_builtin']
      modules = ['openmpi/4.0.3-cuda10.2']
      time_limit = "10m"

      reference = {
                        'ibex' : {
                                'bw_1B' :(2.9,-0.15,None,None),
                                'bw_8K' :(10742,-0.12,None,None),
                                'bw_4M' : (21302,-0.03,None,None)
                                 }
                  }


      @rfm.run_after('init')
      def setting_parameters(self):
           self.executable = 'srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} $OSU_DIR/../get_local_rank $OSU_DIR/pt2pt/osu_mbw_mr -d cuda D D'
           self.sanity_patterns = sn.assert_found(r'^# OSU MPI Multiple Bandwidth / Message Rate Test v5.6.3', self.stdout)
           self.perf_patterns = {
                        'bw_1B': sn.extractsingle(r'^1\s+(?P<bw_1B>\S+)', self.stdout, 1, float),
                        'bw_8K': sn.extractsingle(r'^8192\s+(?P<bw_8K>\S+)', self.stdout, 1, float),
                        'bw_4M': sn.extractsingle(r'^4194304\s+(?P<bw_4M>\S+)', self.stdout, 1, float)
           }

      @rfm.run_before('run')
      def set_job_options(self):
          self.job.options = ['--gpus=4',
                              '--gpus-per-node=1',
#                              '--nodes=1',
                              '--ntasks=4',
                              '--constraint=v100,gpu_ai',
                              '--account=ibex-cs']
