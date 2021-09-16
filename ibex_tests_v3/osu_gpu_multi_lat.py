import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class osu_test(rfm.RunOnlyRegressionTest):
      variant= parameter(['gpu_multi_lat'])
      maintainers = ['passant.hafez@kaust.edu.sa']
      descr = 'running OSU BM on GPUs'
      tags = {'osu_gpu','osu-gpu','osu','latency','lat'}
      sourcesdir= None
      valid_systems = ['ibex:batch']
#      valid_prog_environs = ['gpustack_openmpi']
      valid_prog_environs = ['gpustack_builtin']
      modules = ['openmpi/4.0.3-cuda10.2']
      time_limit = "10m"

      reference = {
                        'ibex' : {
                                'lat_0B' : (2.7,None,0.17,None),
                                'lat_8K' : (5.95,None,0.008,None),
                                'lat_4M' :(422,None,0.03,None),
                                 }
                  }


      @rfm.run_after('init')
      def setting_parameters(self):
           self.executable = 'srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} $OSU_DIR/../get_local_rank $OSU_DIR/pt2pt/osu_multi_lat -d cuda D D'
           self.sanity_patterns = sn.assert_found(r'^# OSU MPI Multi Latency Test v5.6.3', self.stdout)
           self.perf_patterns = {
                        'lat_0B': sn.extractsingle(r'^0\s+(?P<lat_0B>\S+)', self.stdout, 1, float),
                        'lat_8K': sn.extractsingle(r'^8192\s+(?P<lat_8K>\S+)', self.stdout, 1, float),
                        'lat_4M': sn.extractsingle(r'^4194304\s+(?P<lat_4M>\S+)', self.stdout, 1, float)
           }

      @rfm.run_before('run')
      def set_job_options(self):
          self.job.options = ['--gpus=4',
                              '--gpus-per-node=1',
#                              '--nodes=1',
                              '--ntasks=4',
                              '--constraint=v100,gpu_ai',
                              '--account=ibex-cs']

