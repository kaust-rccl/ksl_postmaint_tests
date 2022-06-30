import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class openfoam_test(rfm.RunOnlyRegressionTest):
      variant= parameter(['openfoam_runtime'])
      maintainers = ['passant.hafez@kaust.edu.sa']
      descr = 'running OpenFOAM case'
      tags = {'openfoam','of','cpu'}
      sourcesdir = '../src/openfoam'
      valid_systems = ['ibex:batch']
#      valid_prog_environs = ['gpustack_openmpi']
      valid_prog_environs = ['cpustack_builtin']
      modules = ['openfoam/7.0/gnu-6.4.0']
      time_limit = "10m"
#      num_tasks_per_node = 16
      extra_resources = {'memory': {'size': '64G'}}

      reference = {
                        'ibex' : {
                                'runtime' :(2,None,0.2,None),
                                 }
                  }


      @rfm.run_after('init')
      def setting_parameters(self):
           self.executable = 'mpirun -n 1 blockMesh && mpirun -n 1 decomposePar && time mpirun -n 32 icoFoam -parallel'
           self.sanity_patterns = sn.assert_found(r'^Finalising parallel run', self.stdout)
           self.perf_patterns = {
                        'runtime': sn.extractsingle(r'^user\s+(?P<runtime>\d+)', self.stderr, 1, float),
           }

      @rfm.run_before('run')
      def set_job_options(self):
          self.job.options = ['--nodes=2',
                              '--ntasks=32',
                              '--ntasks-per-node=16',
                              '--ntasks-per-socket=8',
                              '--account=ibex-cs']

