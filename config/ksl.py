# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

#
#

site_configuration = {
    'systems': [
        {
            'name': 'ibex',
            'descr': 'IBEX',
            'hostnames': ['.*'],
            'modules_system': 'tmod4',
            'partitions': [
                {
                    'name': 'login',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'access':  [],
                    'environs': ['cpustack_builtin','cpustack_gnu','cpustack_openmpi','cpustack_intel','cpustack_intelmpi','gpustack_builtin','gpustack_cuda','gpustack_gnu','gpustack_openmpi','gpustack_intel','gpustack_intelmpi'],
                    'descr': 'Login nodes',
                    'max_jobs': 1

                },
                {
                    'name': 'batch',
                    'scheduler': 'slurm',
                    'launcher': 'local',
                    'access':  ['--partition=batch'],
                    'environs': ['cpustack_builtin','cpustack_gnu','cpustack_openmpi','cpustack_intel','cpustack_intelmpi','gpustack_builtin','gpustack_cuda','gpustack_gnu','gpustack_openmpi','gpustack_intel','gpustack_intelmpi'],

                    'descr': 'Mixed nodes',
                    'max_jobs': 32,
                    'resources':[
                            {
                            'name': 'memory',
                            'options': ['--mem={size}']
                            },
                            {
                            'name': 'constraint',
                            'options': ['--constraint={type}']
                            },
                            {
                             'name': '_rfm_gpu',
                             'options': ['--gres=gpu:{num_gpus_per_node}']
                            },
                            {
                             'name': 'nodes',
                             'options': ['--nodes={num_of_nodes}']
                            }

 

                                 ],
                },
                {
                    'name': 'batch_mpi',
                    'scheduler': 'slurm',
                    'launcher': 'mpirun',
                    'access':  ['--partition=batch'],
                    'environs': ['cpustack_builtin','cpustack_gnu','cpustack_openmpi','cpustack_intel','cpustack_intelmpi','gpustack_builtin','gpustack_cuda','gpustack_gnu','gpustack_openmpi','gpustack_intel','gpustack_intelmpi'],

                    'descr': 'Mixed nodes',
                    'max_jobs': 32,
                    'resources':[
                            {
                            'name': 'memory',
                            'options': ['--mem={size}']
                            },
                            {
                            'name': 'constraint',
                            'options': ['--constraint={type}']
                            },
                            {
                             'name': '_rfm_gpu',
                             'options': ['--gres=gpu:{num_gpus_per_node}']
                            },
                            {
                             'name': 'nodes',
                             'options': ['--nodes={num_of_nodes}']
                            }



                                 ],
                },

                {
                    'name': 'gpu',
                    'scheduler': 'slurm',
                    'launcher': 'local',
                    'access':  ['--partition=gpu'],
                    'environs': ['cpustack_builtin','cpustack_gnu','cpustack_openmpi','cpustack_intel','cpustack_intelmpi','gpustack_builtin','gpustack_cuda','gpustack_gnu','gpustack_openmpi','gpustack_intel','gpustack_intelmpi'],

                    'descr': 'Mixed nodes',
                    'max_jobs': 32,
                    'resources':[
                            {
                            'name': 'memory',
                            'options': ['--mem={size}']
                            },
                            {
                            'name': 'constraint',
                            'options': ['--constraint={type}']
                            },
                            {
                             'name': '_rfm_gpu',
                             'options': ['--gres=gpu:{num_gpus_per_node}']
                            },
                            {
                             'name': 'nodes',
                             'options': ['--nodes={num_of_nodes}']
                            }



                                 ],
                },
                
                {
                    'name': 'gpu24',
                    'scheduler': 'slurm',
                    'launcher': 'local',
                    'access':  ['--partition=gpu24'],
                    'environs': ['cpustack_builtin','cpustack_gnu','cpustack_openmpi','cpustack_intel','cpustack_intelmpi','gpustack_builtin','gpustack_cuda','gpustack_gnu','gpustack_openmpi','gpustack_intel','gpustack_intelmpi'],

                    'descr': 'Mixed nodes',
                    'max_jobs': 32,
                    'resources':[
                            {
                            'name': 'memory',
                            'options': ['--mem={size}']
                            },
                            {
                            'name': 'constraint',
                            'options': ['--constraint={type}']
                            },
                            {
                             'name': '_rfm_gpu',
                             'options': ['--gres=gpu:{num_gpus_per_node}']
                            },
                            {
                             'name': 'nodes',
                             'options': ['--nodes={num_of_nodes}']
                            }



                                 ],
                },
                {
                    'name': 'gpu_wide24',
                    'scheduler': 'slurm',
                    'launcher': 'local',
                    'access':  ['--partition=gpu_wide24'],
                    'environs': ['cpustack_builtin','cpustack_gnu','cpustack_openmpi','cpustack_intel','cpustack_intelmpi','gpustack_builtin','gpustack_cuda','gpustack_gnu','gpustack_openmpi','gpustack_intel','gpustack_intelmpi'],

                    'descr': 'Mixed nodes',
                    'max_jobs': 32,
                    'resources':[
                            {
                            'name': 'memory',
                            'options': ['--mem={size}']
                            },
                            {
                            'name': 'constraint',
                            'options': ['--constraint={type}']
                            },
                            {
                             'name': '_rfm_gpu',
                             'options': ['--gres=gpu:{num_gpus_per_node}']
                            },
                            {
                             'name': 'nodes',
                             'options': ['--nodes={num_of_nodes}']
                            }



                                 ],
                },



                {
                    'name': 'debug',
                    'scheduler': 'slurm',
                    'launcher': 'local',
                    'access':  ['--partition=debug'],
                    'environs': ['cpustack_builtin','cpustack_gnu','cpustack_openmpi','cpustack_intel','cpustack_intelmpi','gpustack_builtin','gpustack_cuda','gpustack_gnu','gpustack_openmpi','gpustack_intel','gpustack_intelmpi'],

                    'descr': 'Mixed nodes',
                    'max_jobs': 32,
                    'resources' :[
                            {
                            'name': 'memory',
                            'options': ['--mem={size}']
                            },
                            {
                            'name': 'constraint',
                            'options': ['--constraint={type}']
                            },
                            {
                             'name': '_rfm_gpu',
                             'options': ['--gres=gpu:{num_gpus_per_node}']
                            },
                            {
                             'name': 'nodes',
                             'options': ['--nodes={num_of_nodes}']
                            }

                                ],
                 }

                
            ]
        },
    ],
    'environments': [
        {
            'name':'cpustack_builtin',
            'modules': ['rl9-cpustack'],
            'cc':'',
            'cxx':'',
            'ftn':''
        },

        {
            'name':'cpustack_gnu',
            'modules': ['rl9-cpustack','gcc/12.2.0'],
            'cc': 'gcc',
            'cxx':'g++',
            'ftn': 'gfortran'
        },
        {
            'name':'cpustack_openmpi',
            'modules': ['rl9-cpustack','openmpi/4.1.4/gnu11.2.1'],
            'cc': 'mpicc',
            'cxx':'mpicxx',
            'ftn': 'mpif90'
        },

        { 
            'name':'cpustack_intel',
            'modules': ['rl9-cpustack','intel/2022.3'],
            'cc': 'icc',
            'cxx':'icpc',
            'ftn': 'ifort'
        },

        {
            'name':'cpustack_intelmpi',
            'modules': ['rl9-cpustack','intel/2022.3','mpi/latest'],
            'cc': 'mpiicc',
            'cxx':'mpiicpc',
            'ftn': 'mpifort'
        },
        

        {   
            'name':'gpustack_builtin',
            'modules': ['rl9-gpustack'],
            'cc': '',
            'cxx':'',
            'ftn': ''
        },

        {
            'name':'gpustack_cuda',
            'modules': ['rl9-gpustack','cuda/11.8'],
            'cc': 'nvcc',
            'cxx':'nvcc',
            'ftn': ''
        },
        
        {
            'name':'gpustack_gnu',
            'modules': ['rl9-gpustack','gcc/12.2.0'],
            'cc': 'gcc',
            'cxx':'g++',
            'ftn': 'gfortran'
        },
        {
            'name':'gpustack_openmpi',
            'modules': ['rl9-gpustack','openmpi/4.1.4/gnu11.2.1-cuda11.8'],
            'cc': 'mpicc',
            'cxx':'mpicxx',
            'ftn': 'mpif90'
        },

        {
            'name':'gpustack_intel',
            'modules': ['rl9-gpustack','intel/2022.3'],
            'cc': 'icc',
            'cxx':'icpc',
            'ftn': 'ifort'
        },

        {
            'name':'gpustack_intelmpi',
            'modules': ['rl9-gpustack','intel/2022.3','mpi/latest'],
            'cc': 'mpiicc',
            'cxx':'mpiicpc',
            'ftn': 'mpiifort'
 
        }
        

                 
    ],

            
    'logging': [
        {
            'level': 'debug',
            'handlers': [
                {
                    'type': 'stream',
                    'name': 'stdout',
                    'level': 'info',
                    'format': '%(message)s'
                },


                {
                    'type': 'file',
                    'name': 'reframe.out',
                    'level': 'info',
                    'format': '%(message)s'
                },

                {
                    'type': 'file',
                    'name': 'reframe.log',
                    'level': 'debug',
                    'format': '[%(asctime)s] %(levelname)s: %(check_info)s: %(message)s',   # noqa: E501
                    'append': False
                }
            ],
            'handlers_perflog': [
                {
                    'type': 'filelog',
                    'prefix': '%(check_system)s/%(check_partition)s',
                    'level': 'info',
                    'format': (
                        '%(check_job_completion_time)s|'
                        '%(check_info)s|Jobid=%(check_jobid)s|'
                        'Nodelist=%(check_job_nodelist)s|'
                        '%(check_perf_var)s=%(check_perf_value)s|'
                        'ref=%(check_perf_ref)s'
                        '%(check_perf_unit)s'
                        '(l=%(check_perf_lower_thres)s, '
                        'u=%(check_perf_upper_thres)s)'
                    ),
                    'append': True
               
               },
               {
                    'type': 'stream',
                    'prefix': '%(check_system)s/%(check_partition)s',
                    'level': 'info',
                    'format': (
                        '%(check_name)s|'
                        'Jobid=%(check_jobid)s|'
                        'Nodelist=%(check_job_nodelist)s|'
                        'Performance_Reference=%(check_perf_ref)s'
                        '%(check_perf_unit)s'
                    ),

                 }
 
            ]
        }
    ],
}
