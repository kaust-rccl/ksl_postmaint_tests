import os
# Import reframe pacakge
import reframe as rfm
# Import sanity methods from reframe
import reframe.utility.sanity as sn

# as a Run a pre-compiled executable. Thus path to source code and method of compiling will be required.
@rfm.parameterized_test(['small'],['medium'],['large'],['multinode'])
class gromacs_check(rfm.RunOnlyRegressionTest):
    def __init__(self,variant):
        # Description of test. Should be short but telling
        self.descr = 'GROMACS 2019 SP Run Only tests'
        self.valid_systems = ['ibex:batch']
        self.valid_prog_environs = ['intel']
        
        # sourcesdir is a string which points to where the input files for this test is to be found.
        self.sourcesdir=os.path.join(self.current_system.resourcesdir,'gromacs')
        
        # name of the resulting executable. This will be appended to the resulting srun command line.
        self.executable='gmx_mpi'
        # arguments if the executable "namd2" takes as a list. This is optional
        self.executable_opts="mdrun -deffnm md_0_1".split() 
        
        # JOB SCRIPT attributes

        # you can define your job configuration here: 
        #(Check https://reframe-hpc.readthedocs.io/en/latest/reference.html for all possible options)

        self.time_limit = (0,30,0)  #is a tuple in the format (H,M,S)
        if variant == "small":
          self.num_tasks=8
          self.num_tasks_per_node=8
        elif variant == "medium":  
          self.num_tasks=16
          self.num_tasks_per_node=16 
        elif variant == "large":
          self.num_tasks=40
          self.num_tasks_per_node=40
        else:
          self.num_tasks=128
          self.num_tasks_per_node=40

        # List of modules, if any, to be loaded in the jobscript
        self.modules=['gromacs/2019.4/openmpi-2.1.1-intel-2018-sp']
        # method pre_run adds any commands you wish to run before srun in your jobscript. 
        self.pre_run = ['export OMP_NUM_THREADS=1']
               
        # sanity_patterns is a method to introduce a check on the output file self.stdout (which is slurm-jobid.out).
        # sanity check is a way to know that the simulation has started in a normal fashion. 
        # see list of possible sanity function here https://reframe-hpc.readthedocs.io/en/latest/sanity_functions_reference.html
        #self.sanity_patterns = sn.assert_found(r':-) GROMACS - gmx mdrun, 2019.4 (-:', 'rfm_gromacs_check_job.err', encoding='utf-8')
        self.sanity_patterns = sn.assert_found(r'\s+:-\) GROMACS - gmx mdrun, 2019.4 \(-:', self.stderr, encoding='utf-8')
        
        # perf_pattern is a method to capture the performance metric from the output file self.stdout (or any other filename with relative path)
        self.perf_patterns = {       
                    variant: sn.extractsingle(r'^Performance:\s+(?P<ns_day>\S+)', self.stderr, 'ns_day', float)
                               }
        
        # the captured metric in perf_patterns needs to be compared with a reference 
        # value for reporting status of the test
        # For this the reference value with a range +/- percent is expected. 
        # For example (0.027,-0.005,0.005) implies that the performance quantity should 
        # be 0.37 with tolerance of -10% or +10%
        self.reference = {
                            'ibex' : {    
                               'small': (28, -0.15, 0.15),
                               'medium': (49, -0.15, 0.15),
                               'large': (98, -0.15, 0.15),
                               'multinode': (216, -0.15, 0.15),
                 
                                     },
                            }
        
        
        # tags are useful to filter tests when not all but specific the tests are suppose to run
        self.tags = {'gromacs','gromacs_'+variant,'acceptance'}
        
        # initials or email of the maintainer    
        #self.maintainers = ['MS']
