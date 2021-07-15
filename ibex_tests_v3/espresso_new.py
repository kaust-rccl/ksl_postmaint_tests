import os

import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class espresso(rfm.RunOnlyRegressionTest):
      variant= parameter(['single', 'multi'])
      @rfm.run_after('init')
      def setting_variables(self):

        self.maintainers = ['amr.radwan@kaust.edu.sa']
        self.tags = {'espresso'}
        self.valid_systems = ['ibex:batch_mpi']
        self.sourcesdir = '../src/espresso'

        self.valid_prog_environs = ['cpustack_builtin']
        self.modules=['quantumespresso/6.4.1/openmpi3.0.0-intel17']
        self.executable = 'pw.x'
        self.executable_opts = ['-in', 'qe.scf.in']
        self.time_limit='10m'
        energy = sn.extractsingle(r'!\s+total energy\s+=\s+(?P<energy>\S+) Ry',
                                  self.stdout, 'energy', float)
        self.sanity_patterns = sn.all([
            sn.assert_found(r'convergence has been achieved', self.stdout),
            sn.assert_reference(energy, -62.96497971)
        ])
        self.perf_patterns = {
            'time': sn.extractsingle(r'electrons    :\s+(?P<sec>\S+)s CPU ',
                                     self.stdout, 'sec', float)
        }
        if self.variant == 'single':
            self.num_tasks = 32
            self.descr = 'Quantum Espresso CPU check on Single Node'
            self.num_tasks_per_node = 32
            self.reference = {
                'ibex:batch_mpi': {
                    'time': (0.77, None, 0.05, 's'),
                }
            }
        else:
            self.num_tasks = 32
            self.descr = 'Quantum Espresso CPU check on Multi Node'
            self.num_tasks_per_node = 16
            self.reference = {
                'ibex:batch_mpi': {
                    'time': (0.9, None, 0.05, 's')
                }
            }
