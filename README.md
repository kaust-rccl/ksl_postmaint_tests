## Reframe 4.4.1 on RL9

ReFrame is a high-level framework for writing regression tests for HPC systems written in Python3.x and is authored and maintained by CSCS. 
We are prototyping ReFrame on IBEX to use it as a post-maintenance testing suit to run on IBEX.
This repositary contains tests for RL9. 

Reframe v4.4.1 with python 3.11.0 is installed can be accessed via the following module
```sh
module load reframe/4.4.1
```
To list the tests 
```sh
reframe -c rl9-tests-v4 -l 
```
To run The  all tests
```sh
reframe -c rl9-tests-v4 -r 
```
To run the tests under Maintaince 
```sh
reframe -c rl9-tests-v4  -Jreservation=<reservation_name> -r 
```

