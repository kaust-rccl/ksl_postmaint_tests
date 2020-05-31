#
# ReFrame settings for KSL systems
#
import os
class ReframeSettings:
	job_poll_intervals = [1, 2, 3]
	job_submit_timeout = 60
	checks_path = ['checks/']
	checks_path_recurse = True
	# Check if the Resources directory is in a non standard path, if not then set it to the default path as is expected to be the Reframe installation directory.
	if os.getenv('REFRAME_RESOURCE_DIR') is None:
	REFRAME_RESOURCE_DIR = os.path.join(os.getenv('PWD'), 'resourcesdir')
	else:
	REFRAME_RESOURCE_DIR = os.getenv('REFRAME_RESOURCE_DIR')

	site_configuration = {
		'systems': {
			'ibex': {
				'descr': 'IBEX',
				'hostnames': ['glogin', 'ilogin', 'slogin'],
				'modules_system': 'tmod',
				'resourcesdir': REFRAME_RESOURCE_DIR,
				'partitions': {
					'login': {
						'scheduler': 'local',
						'modules': [],
						'access':  [],
						'environs': ['builtin-gcc'],
						'descr': 'Login nodes',
						'max_jobs': 1
					},

					'batch': {
						'scheduler': 'slurm+mpirun',
						'modules': [],
						'access':  ['--partition=batch'],
						'environs': ['gnu', 'intel', 'gnu_cuda'],
						'descr': 'Mixed nodes',
						'max_jobs': 32,
						'resources': {
							'_rfm_gpu': ['--gres=gpu:{num_gpus_per_node}']
						},
						'container_platform': {
							'Singularity': {
								'modules': ['singularity/3.5']
							}
						}
					},
					'debug': {
						'scheduler': 'slurm+mpirun',
						'modules': [],
						'access':  ['--partition=debug'],
						'environs': ['gnu', 'intel', 'gnu_cuda'],
						'descr': 'Mixed nodes',
						'max_jobs': 32,
						'resources': {
							'_rfm_gpu': ['--gres=gpu:{num_gpus_per_node}']
						},
						'container_platform': {
							'Singularity': {
								'modules': ['singularity/3.5']
							}
						} 
					},
				},
			},
		},

		'environments': {
			'ibex': {
				'gnu': {
					'type': 'ProgEnvironment',
					'modules': ['gcc/6.4.0', 'openmpi/4.0.1/gnu-6.4.0'],
					'cc':'mpicc',
					'cxx':'mpicxx',
					'ftn':'mpif90'
				},
				'gnu_cuda': {
					'type': 'ProgEnvironment',
					'modules': ['gpustack','gcc/6.4.0', 'cuda/10.1.105', 'openmpi/4.0.1/gnu6.4.0_cuda10.1.105'],
					'cc':'mpicc',
					'cxx':'mpicxx',
					'ftn':'mpif90'
				},
				'intel': {
					'type': 'ProgEnvironment',
					'modules': ['intelstack-default'],
					'cc':'mpicc',
					'cxx':'mpicxx',
					'ftn':'mpif90'
				},
				'intel_cuda': {
					'type': 'ProgEnvironment',
					'modules': ['gpustack'],
					'cc':'mpicc',
					'cxx':'mpicxx',
					'ftn':'mpif90'
				},
				'builtin-gcc': {
					'type': 'ProgEnvironment',
					'cc':  'gcc',
					'cxx': 'g++',
					'ftn': 'gfortran',
				}
			},
		},

		'modes': {
			'*': {
				'maintenance': [
				'--exec-policy=async',
				'--strict',
				'--output=$APPS/UES/$USER/regression/maintenance',
				'--logdir=$APPS/UES/$USER/regression/maintenance/logs',
				'--stage=$SCRATCH/regression/maintenance/stage',
				'--reservation=maintenance',
				'--save-log-files',
				'--tag=maintenance',
				'--timestamp=%F_%H-%M-%S'
				],
				'production': [
					'--exec-policy=async',
				'--strict',
				'--output=$APPS/UES/$USER/regression/production',
				'--logdir=$APPS/UES/$USER/regression/production/logs',
				'--stage=$SCRATCH/regression/production/stage',
				'--save-log-files',
				'--tag=production',
				'--timestamp=%F_%H-%M-%S'
				]
			}
		}
	}

logging_config = {
	'level': 'DEBUG',
	'handlers': [
	{
		'type': 'file',
		'name': 'reframe.log',
		'level': 'DEBUG',
		'format': '[%(asctime)s] %(levelname)s: '
			'%(check_name)s: %(message)s',
		'append': False,
	},

	# Output handling
	{
		'type': 'stream',
		'name': 'stdout',
		'level': 'INFO',
		'format': '%(message)s'
	},
	{
		'type': 'file',
		'name': 'reframe.out',
		'level': 'INFO',
		'format': '%(message)s',
		'append': False,
	}
	]
}

perf_logging_config = {
	'level': 'DEBUG',
	'handlers': [
	{
		'type': 'filelog',
		# 'type': 'graylog',
		# 'host': 'my.graylog.server',
		# 'port': 12345,
		'prefix': '%(check_system)s/%(check_partition)s',  # Not needed for graylog
			'level': 'INFO',
		'format': (
				'%(asctime)s|reframe %(version)s|'
				'%(check_info)s|jobid=%(check_jobid)s|'
				'%(check_perf_var)s=%(check_perf_value)s|'
				'ref=%(check_perf_ref)s '
				'(l=%(check_perf_lower_thres)s, '
					'u=%(check_perf_upper_thres)s)'
			  ),
		'append': True
			# 'extras': {
				#    'facility': 'reframe',
				# }
	}
	]
}


settings = ReframeSettings()
