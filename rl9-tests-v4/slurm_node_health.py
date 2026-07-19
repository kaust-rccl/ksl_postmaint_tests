import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.simple_test
class slurm_node_health(rfm.RunOnlyRegressionTest):
    @run_after('init')
    def set_variables(self):
        self.descr = 'SLURM node health check: detailed node information via sinfo'
        self.valid_systems = ['ibex:login', 'ibex:batch']
        self.valid_prog_environs = ['cpustack_builtin']
        self.sourcesdir = None
        self.num_tasks = 1
        self.time_limit = '3m'
        self.maintainers = ['moamen.mohamed@kaust.edu.sa']
        self.tags = {'slurm', 'node_health', 'cpu', 'singlenode'}

    @run_after('setup')
    def generate_sinfo_script(self):
        script_path = os.path.join(self.stagedir, 'node_health.sh')
        with open(script_path, 'w') as fp:
            fp.write('''#!/bin/bash
echo "========================================="
echo "Slurmd Health Check"
echo "Time: $(date)"
echo "========================================="
echo ""
echo "========================================="
echo "Detailed Node Health Information"
echo "========================================="
sinfo -N -o "%N %t %m %e %a %c %C %G %D %O"
''')
        os.chmod(script_path, 0o755)
        self.executable = script_path
        self.executable_opts = []

        self.sanity_patterns = sn.all([
            sn.assert_found(r'NODELIST\s+STATE\s+MEMORY\s+FREE_MEM\s+AVAIL\s+CPUS\s+CPUS\(A/I/O/T\)\s+GRES\s+NODES\s+CPU_LOAD', self.stdout),
            sn.assert_gt(sn.count(sn.findall(r'^[a-zA-Z0-9\-_]+\.?[a-z0-9\-]*\s+', self.stdout)), 0)
        ])
