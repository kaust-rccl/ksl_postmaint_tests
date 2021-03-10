import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.parameterized_test(['latency'],['bandwidth'],['bibandwidth'])
class osu_test(rfm.RunOnlyRegressionTest):
	def __init__(self,variant):



		## TEST BASIC INFO
		self.maintainers = ['passant.hafez@kaust.edu.sa']
		self.descr = 'running OSU BM'
		self.tags = {'osu'}



		## SETTING UP TEST ENV
		self.sourcesdir= None
                #self.valid_prog_environs = ['builtin-gcc']
                #self.valid_prog_environs = ['batch_nompi']
		self.valid_prog_environs = ['gnu']
		self.valid_systems = ['ibex:batch']

		#self.pre_run = ['module use /ibex/scratch/projects/swtools/modulefiles','module load osu-microbenchmarks/5.6.2','module load openmpi/4.0.3']
		self.modules = ['openmpi/4.0.3','/ibex/scratch/projects/swtools/modulefiles/osu-microbenchmarks/5.6.2']
		#self.modules = ['openmpi/4.0.3']



		## SLURM
		self.time_limit = (0,10,0)
		self.num_tasks = 2
		self.num_tasks_per_node = 1



		## RUN & VALIDATE

		if variant == "latency":
			self.executable='osu_latency'
			self.sanity_patterns = sn.assert_found(r'^# OSU MPI Latency Test v5.6.2', self.stdout)
			#self.perf_patterns = {variant: sn.extractsingle(r'^0\s+(?P<0Blat>\S+)',self.stdout, '0Blat', float)}
			self.perf_patterns = {
				variant: sn.extractsingle(r'^4194304\s+(?P<FourGBlat>\S+)',self.stdout, 'FourGBlat', float)}
			#self.reference = 

		elif variant == "bandwidth":
			self.executable='osu_bw'
			self.sanity_patterns = sn.assert_found(r'^# OSU MPI Bandwidth Test v5.6.2', self.stdout)
			#self.perf_patterns = {variant: sn.extractsingle(r'^0\s+(?P<0Bbw>\S+)',self.stdout, '0Bbw', float)}
			self.perf_patterns = {variant: sn.extractsingle(r'^4194304\s+(?P<FourGBbw>\S+)',self.stdout, 'FourGBbw', float)}
			#self.reference = 

		elif variant == "bibandwidth":
			self.executable='osu_bibw'
			self.sanity_patterns = sn.assert_found(r'^# OSU MPI Bi-Directional Bandwidth Test v5.6.2', self.stdout)
			#self.perf_patterns = {variant: sn.extractsingle(r'^0\s+(?P<0Bbibw>\S+)',self.stdout, '0Bbibw', float)}
			self.perf_patterns = {variant: sn.extractsingle(r'^4194304\s+(?P<FourGBbibw>\S+)',self.stdout, 'FourGBbibw', float)}
			#self.reference = 


		self.reference = {
			'ibex' : {
				'latency' : (390.0,None,0.1),
				'bandwidth' : (12000.0,-0.1,None),
				'bibandwidth' : (24000.0,-0.1,None),
			},
		}

