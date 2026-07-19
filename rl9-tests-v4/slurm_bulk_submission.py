import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.simple_test
class slurm_bulk_submission(rfm.RunOnlyRegressionTest):
    @run_after('init')
    def set_variables(self):
        self.descr = 'SLURM bulk submission test: submit 60 short jobs'
        self.valid_systems = ['ibex:batch']
        self.valid_prog_environs = ['cpustack_builtin']
        self.sourcesdir = None
        self.num_tasks = 1
        self.time_limit = '10m'
        self.maintainers = ['moamen.mohamed@kaust.edu.sa']
        self.tags = {'slurm', 'bulk_submission', 'cpu', 'singlenode'}

    @run_after('setup')
    def generate_submit_script(self):
        script = os.path.join(self.stagedir, 'submit_60.sh')
        with open(script, 'w') as f:
            f.write('''#!/bin/bash
			submitted=0
			for i in $(seq 1 60); do
    				if sbatch --time=00:10:00 --output="output/database_stress/%j_%N.out" --wrap="sleep 5" &>/dev/null; then
	        			((submitted++))
    				fi
			done
			echo "Submitted ${submitted} stress test jobs"
		''')
        os.chmod(script, 0o755)
        self.executable = script
        self.sanity_patterns = sn.assert_found(r'^Submitted 60 stress test jobs$', self.stdout)
