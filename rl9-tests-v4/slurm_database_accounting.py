import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.simple_test
class slurm_database_accounting(rfm.RunOnlyRegressionTest):
    @run_after('init')
    def set_variables(self):
        self.descr = 'SLURM accounting test: submit job and verify sacct records'
        self.valid_systems = ['ibex:batch']
        self.valid_prog_environs = ['cpustack_builtin']
        self.sourcesdir = None
        self.num_tasks = 1
        self.time_limit = '5m'
        self.maintainers = ['moamen.mohamed@kaust.edu.sa']
        self.tags = {'slurm', 'database_accounting', 'cpu', 'singlenode'}

    @run_after('setup')
    def generate_script(self):
        script_path = os.path.join(self.stagedir, 'check_accounting.sh')
        with open(script_path, 'w') as f:
            f.write('''#!/bin/bash
			set -e
			JOB_ID=$(sbatch --time=00:02:00 --wrap="sleep 60" | awk '{print $4}')
			echo "Job ID: $JOB_ID"

			while true; do
			    STATE=$(sacct --noheader --format=state -j $JOB_ID 2>/dev/null | awk '{print $1}' | head -1)
			    case "$STATE" in
			        COMPLETED|FAILED|CANCELLED|TIMEOUT)
		            echo "Job finished with state: $STATE"
            		break
            		;;
		        *)
            		sleep 5
		            ;;
			    esac
			done

			sacct -j $JOB_ID --format=JobID,State,ExitCode,NodeList,Start,End --noheader
		''')
        os.chmod(script_path, 0o755)
        self.executable = script_path
        self.executable_opts = []

        self.sanity_patterns = sn.all([
            sn.assert_found(r'COMPLETED', self.stdout),
            sn.assert_found(r'0:0', self.stdout)
        ])
