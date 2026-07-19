import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.simple_test
class slurm_job_dependency(rfm.RunOnlyRegressionTest):
    @run_after('init')
    def set_variables(self):
        self.descr = 'SLURM job dependency test: afterok'
        self.valid_systems = ['ibex:batch']
        self.valid_prog_environs = ['cpustack_builtin']
        self.sourcesdir = None
        self.num_tasks = 1
        self.time_limit = '15m'          
        self.maintainers = ['moamen.mohamed@kaust.edu.sa']
        self.tags = {'slurm', 'dependency', 'cpu', 'singlenode'}

    @run_after('setup')
    def generate_dependency_script(self):
        script_path = os.path.join(self.stagedir, 'job_dependency.sh')
        with open(script_path, 'w') as fp:
            fp.write('''#!/bin/bash
			set -e

			OUTDIR="${PWD}/job_outputs"
			mkdir -p "$OUTDIR"

			echo "Submitting primary job (sleep 30)..."
			PRIMARY_ID=$(sbatch --time=00:10:00 --output="$OUTDIR/primary_%j.out" --wrap="sleep 30" | awk '{print $4}')
			echo "Primary job ID: $PRIMARY_ID"

			echo "Submitting dependent job (afterok:$PRIMARY_ID)..."
			DEP_ID=$(sbatch --time=00:10:00 --dependency=afterok:$PRIMARY_ID --output="$OUTDIR/dependent_%j.out" --wrap="echo done after $PRIMARY_ID" | awk '{print $4}')
			echo "Dependent job ID: $DEP_ID"

			echo "Waiting for dependent job to finish..."
			while true; do
    				STATE=$(sacct --noheader --format=state -j $DEP_ID 2>/dev/null | head -1 | awk '{print $1}')
    				case "$STATE" in
        				COMPLETED|FAILED|CANCELLED|TIMEOUT)
            				echo "Dependent job finished with state: $STATE"
            			break
            		;;
        		*)
            		sleep 5
            		;;
    			esac
		done

		DEP_OUTPUT="$OUTDIR/dependent_${DEP_ID}.out"
		if [ -f "$DEP_OUTPUT" ]; then
		    cat "$DEP_OUTPUT"
		    echo "======================================="
		else
		    echo "ERROR: Dependent job output file not found: $DEP_OUTPUT"
		    exit 1
		fi
		''')
        os.chmod(script_path, 0o755)
        self.executable = script_path
        self.executable_opts = []

        self.sanity_patterns = sn.assert_found(r'done after \d+', self.stdout)
