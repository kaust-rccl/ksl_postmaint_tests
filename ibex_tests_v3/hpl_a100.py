import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class hpl_tests(rfm.RunOnlyRegressionTest):

      variant= parameter(['a100_4_singlenode'])


           ## TEST BASIC INFO
      maintainers = ['rana.selim@kaust.edu.sa']
      descr = 'running hpl tests for a100'
      path = variable(str)
      #gflops = variable(float)
           ## SETTING TEST ENV
      sourcesdir= None
      valid_prog_environs = ['gpustack_builtin']
      valid_systems = ['ibex:batch']
      reference = {
                        'ibex' : {
                               'a100_4_singlenode' : (56000,-0.06,None,'Gflops')

                        }
                }
      
          ## RUN AND VALIDATE
      @rfm.run_after('init')
      def setting_variables(self):
        self.path='HPL.out'
        if self.variant == 'a100_4_singlenode': 
           self.time_limit = '2h'
           self.num_tasks=4
           self.num_gpus_per_node=4
           self.extra_resources = {'memory': {'size': '450G'},'constraint': {'type': 'a100'},'nodes': {'num_of_nodes': '1'}}
           self.executable='srun -u -n ${SLURM_NTASKS} -c ${CPUS} --cpu-bind=map_cpu:48-55,32-39,16-23,2-9 singularity run --nv $IMAGE hpl.sh --cpu-affinity +48-55:32-39:16-23:2-9 --cpu-cores-per-rank ${CPUS} --gpu-affinity 3:2:1:0 --dat ./HPL.dat.a100.G4N1'
           self.num_cpus_per_task=14
           
           self.prerun_cmds = ['module purge','module load gpustack','module load singularity','module load openmpi/4.0.3-cuda11.2.2','export IMAGE=./hpl_sing.sif','export CPUS=8','export OMPI_MCA_btl_openib_warn_no_device_params_found=0']

           self.sourcesdir='../src/hpl/'
           self.tags = {'hpl','gpu',self.variant,'acceptance'}

                

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
     


