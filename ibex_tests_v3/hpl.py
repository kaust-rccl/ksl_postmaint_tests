import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class hpl_tests(rfm.RunOnlyRegressionTest):

      variant= parameter(['v100_8_singlenode', 'v100_8_multinode','a100_8_singlenode','a100_8_multinode'])


           ## TEST BASIC INFO
      maintainers = ['rana.selim@kaust.edu.sa']
      descr = 'running hpl tests'

           ## SETTING TEST ENV
      sourcesdir= None
      valid_prog_environs = ['gpustack_builtin']
      valid_systems = ['ibex:batch_mpi']
      #modules = ['singularity','openmpi/4.0.3-cuda11.2.2']
      reference = {
                        'ibex' : {
                                'v100_8_singlenode' : (100,None,+2,'GB/s'),
                                'a100_8_singlenode' :(150,None,+2,'GB/s'),
                                'v100_8_multinode' : (5.00000,None,+2,'GB/s'),
                                'a100_8_multinode' : (13.00000,None,+2,'GB/s')

                        }
                }
      
          ## RUN AND VALIDATE
      @rfm.run_after('init')
      def setting_variables(self):
        if self.variant == 'v100_8_singlenode': 
           self.time_limit = '1h'
           self.num_tasks=8
           self.extra_resources = {'memory': {'size': '700G'}}          
           self.executable='--bind-to none --nooversubscribe singularity run --nv $IMAGE hpl.sh --cpu-cores-per-rank ${CPUS} \
--cpu-affinity 2-5:6-9:10-13:14-17:24-27:28-31:32-37:38-41 \
--gpu-affinity 0:1:2:3:4:5:6:7 --dat  ./HPL.dat.v100.G8N1'
           self.num_cpus_per_task=5
           #self.num_gpus_per_node=8
           self.extra_resources = {'constraint': {'type': 'v100'}}
           
           self.prerun_cmds = ['module purge','module load gpustack','module load singularity','module load openmpi/4.0.3-cuda11.2.2','export IMAGE=./hpc-benchmarks_21.4-hpl.sif','export CPUS=4','export RUNDIR=HPL_${SLURM_JOBID}','mkdir -p $RUNDIR','cd $RUNDIR']
# '
#,'export IMAGE=${BASE}/../src/hpc-benchmarks_21.4-hpl.sif','export RUNDIR=HPL_${SLURM_JOBID}'
#,'mkdir -p $RUNDIR','cp ${BASE}/../src/HPL.dat.v100.G8N1 HPL.dat']
           self.sourcesdir='../src/hpl/v100.G8N1'

        elif self.variant == 'a100_8_singlenode':
           self.time_limit = '30m'
           self.num_tasks=1
           self.executable='all_reduce_perf -g 8 -o all -c 1 -f 2 -d all'
           self.num_cpus_per_task=46
           self.num_gpus_per_node=8
           self.extra_resources = {'constraint': {'type': 'a100'}}

        
             
        elif self.variant == 'v100_8_multinode':

           self.num_tasks=2
           self.time_limit = '2h'
           self.extra_resources = {'constraint': {'type': 'v100'}}
           self.num_cpus_per_task=46
           self.executable='srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} --cpu-bind=cores    all_reduce_perf -b 8 -e 256M -f 2 -g 8 -c 1 -n 50 -w 20'
           self.prerun_cmds = ['export NCCL_DEBUG=INFO','export UCX_TLS=tcp','hostname','module list']
           #self.num_gpus_per_node=8


        elif self.variant == 'a100_8_multinode':

           self.num_tasks=2
           self.time_limit = '2h'
           self.extra_resources = {'constraint': {'type': 'a100'}}
           self.num_cpus_per_task=46
           self.executable='srun -n ${SLURM_NTASKS} -N ${SLURM_NNODES} --cpu-bind=cores    all_reduce_perf -b 8 -e 256M -f 2 -g 8 -c 1 -n 50 -w 20'
           self.prerun_cmds = ['export NCCL_DEBUG=INFO','export UCX_TLS=tcp','hostname','module list']
          # self.num_gpus_per_node=8


        self.tags = {'gpu',self.variant,'acceptance'}

                
    


      @rfm.run_before('run')
      def set_job_options(self):
        if self.variant== 'v100_8_singlenode':
           self.job.options = ['--gpus=8','--gpus-per-node=8']
        elif self.variant== 'a100_8_multinode':
           self.job.options = ['--gpus=8','--gpus-per-node=8']



      @rfm.run_before('sanity')
      def set_sanity_patterns(self):
          self.sanity_patterns = sn.assert_found(r'# Avg bus bandwidth', self.stdout)
         

      #@rfm.run_before('performance')
      #def set_perf_patterns(self):
      #    self.perf_patterns = {self.variant : sn.extractsingle(r'^#\s[A]\w+\s\w+\s\w+\s+[:]\s(?P<Busbw>\d*\.\d+)', self.stdout, 'Busbw' , float)}
