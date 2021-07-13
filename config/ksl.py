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
            'modules_system': 'tmod32',
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
                            'options': ['--constraint={value}']
                            },
                            {
                             'name': 'gres',
                             'options': ['--gres=gpu:{num_gpus_per_node}']
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
                            'options': ['--constraint={value}']
                            },
                            {
                             'name': 'gres',
                             'options': ['--gres=gpu:{num_gpus_per_node}']
                            }
                                ],
                 }
                
            ]
        },
    ],
    'environments': [
        {
            'name':'cpustack_builtin',
            'modules': ['default-appstack'],
            'cc':'',
            'cxx':'',
            'ftn':''
        },

        {
            'name':'cpustack_gnu',
            'modules': ['default-appstack','gcc/6.4.0'],
            'cc': 'gcc',
            'cxx':'g++',
            'ftn': 'gfortran'
        },
        {
            'name':'cpustack_openmpi',
            'modules': ['default-appstack','openmpi/4.0.3'],
            'cc': 'mpicc',
            'cxx':'mpicxx',
            'ftn': 'mpif90'
        },

        { 
            'name':'cpustack_intel',
            'modules': ['default-appstack','intel/2020'],
            'cc': 'icc',
            'cxx':'icpc',
            'ftn': 'ifort'
        },

        {
            'name':'cpustack_intelmpi',
            'modules': ['default-appstack','intel/2020','intelmpi/2020'],
            'cc': 'mpiicc',
            'cxx':'mpiicpc',
            'ftn': 'mpifort'
        },
        

        {   
            'name':'gpustack_builtin',
            'modules': ['gpustack'],
            'cc': '',
            'cxx':'',
            'ftn': ''
        },

        {
            'name':'gpustack_cuda',
            'modules': ['gpustack','cuda/11.2.2'],
            'cc': 'nvcc',
            'cxx':'nvcc',
            'ftn': ''
        },
        
        {
            'name':'gpustack_gnu',
            'modules': ['gpustack','gcc/6.4.0'],
            'cc': 'gcc',
            'cxx':'g++',
            'ftn': 'gfortran'
        },
        {
            'name':'gpustack_openmpi',
            'modules': ['gpustack','openmpi/4.0.3-cuda11.0'],
            'cc': 'mpicc',
            'cxx':'mpicxx',
            'ftn': 'mpif90'
        },

        {
            'name':'gpustack_intel',
            'modules': ['gpustack','intel/2020'],
            'cc': 'icc',
            'cxx':'icpc',
            'ftn': 'ifort'
        },

        {
            'name':'gpustack_intelmpi',
            'modules': ['gpustack','intel/2020','intelmpi/2020'],
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
                        '%(check_job_completion_time)s|reframe %(version)s|'
                        '%(check_info)s|jobid=%(check_jobid)s|'
                        '%(check_perf_var)s=%(check_perf_value)s|'
                        'ref=%(check_perf_ref)s '
                        '(l=%(check_perf_lower_thres)s, '
                        'u=%(check_perf_upper_thres)s)|'
                        '%(check_perf_unit)s'
                    ),
                    'append': True
                }
            ]
        }
    ],
}
