import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class osu_test(rfm.RunOnlyRegressionTest):
      variant= parameter(['latency', 'bandwidth','bibandwidth'])
      maintainers = ['passant.hafez@kaust.edu.sa']
      descr = 'running OSU BM'
      tags = {'osu','cpu','acceptance'}
      sourcesdir= None
      valid_prog_environs = ['cpustack_gnu']
      valid_systems = ['ibex:batch_mpi']
      #modules = ['openmpi/4.0.3','/ibex/scratch/projects/swtools/modulefiles/osu-microbenchmarks/5.7.1']
      modules = ['openmpi/4.0.3']
      time_limit = "10m"
      num_tasks = 2
      num_tasks_per_node = 1
      reference = {
                        'ibex' : {
                                'latency' : (390.0,None,0.1,None),
                                'bandwidth' : (12000.0,-0.1,None,None),
                                'bibandwidth' : (24000.0,-0.1,None,None),
                                 }
                        }


      @rfm.run_after('init')
      def setting_parameters(self):
        if self.variant == "latency":
           self.executable='osu_latency'
           self.sanity_patterns = sn.assert_found(r'^# OSU MPI Latency Test v5.7.1', self.stdout)
           self.perf_patterns = {
                                self.variant: sn.extractsingle(r'^4194304\s+(?P<FourGBlat>\S+)',self.stdout, 'FourGBlat', float)}

        
        elif self.variant == "bandwidth":
           self.executable='osu_bw'
           self.sanity_patterns = sn.assert_found(r'^# OSU MPI Bandwidth Test v5.7.1', self.stdout)
           self.perf_patterns = {self.variant: sn.extractsingle(r'^4194304\s+(?P<FourGBbw>\S+)',self.stdout, 'FourGBbw', float)}

        elif self.variant == "bibandwidth":
           self.executable= 'osu_bibw'
           self.sanity_patterns = sn.assert_found(r'^# OSU MPI Bi-Directional Bandwidth Test v5.7.1', self.stdout)
           self.perf_patterns = {self.variant: sn.extractsingle(r'^4194304\s+(?P<FourGBbibw>\S+)',self.stdout, 'FourGBbibw', float)}

