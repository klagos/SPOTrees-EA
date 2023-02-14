# SPOTrees Original

Original implementation retrieved from https://github.com/rtm2130/SPOTree.

Experiments with the following parameters:

* n_train : 200
* eps : 0
* deg_set_str : 2-10
* reps_st: 0
* reps_end: 10
* max_depth: 3
* min_weights_per_node: 20
* algtype: SPO

Tuned parameters:

*
*
*
*

To make an experiment the dataset must be in the same folder and the C++ code for the evolutionary algorithm has to be compiled (both paths can be modified). Then run on the command line:

`python SPOEA.py 200 0 2-10 0 10 3 20 SPO`



