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
* algtype: SPO/MSE

To make an experiment the dataset must be in the same folder (or the path must be modified) and dimension has to be edited in the file (line 68). Then run on the command line:

* SPO: `python SPOgreedy_nonlinear.py 200 0 2-10 0 10 3 20 SPO`

* CART: `python SPOgreedy_nonlinear.py 200 0 2-10 0 10 3 20 MSE`

