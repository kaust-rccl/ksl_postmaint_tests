## Reframe 3.6.0 on Ibex 

ReFrame is a high-level framework for writing regression tests for HPC systems.written in Python3.x and is authored and maintained by CSCS. 
We are prototyping ReFrame on IBEX to use it as a post-maintenance testing suit for all relevant personals to run on IBEX as themselves.

# Reframe v3.6.0 with python 3.8.1 is installed can be accessed via the following module
```sh
module load reframe/3.6.0
```
To list the tests 
```sh
reframe -c ibex_tests_v3 -l 
```
To run The  all tests
```sh
reframe -c ibex_tests_v3 -r 
```
To run specific Tests 
```sh
reframe -c ibex_tests_v3 -n osu  -r 
```
To run the tests under Maintaince 
```sh
reframe -c ibex_tests_v3 -Jreservation=<reservation_name> -r 
```
## New features and enhancements in v 3.6.0

- Deprecate the use of the @parameterized_test decorator 
- The old syntax of defining timelimit using a (h, m, s) tuple is deprecated.
```sh
self.time_limit = '30m'
self.time_limit = '2h'
```
- The prebuild_cmd, postbuild_cmd, pre_run and post_run attributes have been removed
```sh
self.prerun_cmds = ['hostname','module list']
```


