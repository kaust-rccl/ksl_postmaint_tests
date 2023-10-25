import os
# Import reframe pacakge
import reframe as rfm
# Import sanity methods from reframe
import reframe.utility.sanity as sn

# as a Run a pre-compiled executable. Thus path to source code and method of compiling will be required
@rfm.simple_test
class gromacs_tests(rfm.RunOnlyRegressionTest):
      variant= parameter(['small', 'medium','large','multinode'])
      reference = {
                     'ibex' : {
                       'small': (35, -0.15, None,'ns_day'),
                       'medium': (74, -0.15, None,'ns_day'),
                       'large': (140, -0.15, None,'ns_day'),
                       'multinode': (70, -0.15, None,'ns_day')

                                     }
                            }



      @run_after('init')
      def setting_variables(self):


        # Description of test. Should be short but telling
        self.descr = 'GROMACS 2023 SP Run Only tests'
        self.valid_systems = ['ibex:batch_mpi']
        self.valid_prog_environs = ['cpustack_builtin']
        
        # sourcesdir is a string which points to where the input files for this test is to be found.
        self.sourcesdir='../src/gromacs'
        
        # name of the resulting executable. This will be appended to the resulting srun command line.
        self.executable='gmx_mpi'
        # arguments if the executable "namd2" takes as a list. This is optional
        self.executable_opts="mdrun -deffnm md_0_1".split() 
        
        # JOB SCRIPT attributes

        # you can define your job configuration here: 
        #(Check https://reframe-hpc.readthedocs.io/en/latest/reference.html for all possible options)

        self.time_limit = "30m" #is a tuple in the format (H,M,S)
        if self.variant == "small":
          self.num_tasks=8
          self.num_tasks_per_node=8
        elif self.variant == "medium":  
          self.num_tasks=16
          self.num_tasks_per_node=16 
        elif self.variant == "large":
          self.num_tasks=40
          self.num_tasks_per_node=40
        else:
          self.num_tasks=16
          self.num_tasks_per_node=8

        self.modules=['gromacs/2023/openmpi-4.1.4-intel-2022.3-sp','gcc/12.2.0']

        self.prerun_cmds  = ['export OMP_NUM_THREADS=1']
               
        self.sanity_patterns = sn.assert_found(r'\s+:-\) GROMACS - gmx mdrun, 2023 \(-:', self.stderr, encoding='utf-8')
        self.perf_patterns = {       
                   self.variant: sn.extractsingle(r'^Performance:\s+(?P<ns_day>\S+)', self.stderr, 'ns_day', float)
                               }
        
#tags are useful to filter tests when not all but specific the tests are suppose to run
        self.tags = {'gromacs','gromacs_'+self.variant,'acceptance','cpu'}
        

