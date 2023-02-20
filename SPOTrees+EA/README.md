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
* seed: [53162, 44260, 31005, 6078, 78362, 98202, 41236, 63404, 81087, 86108]
* dimension: [5, 7, 10, 15] 

Tuned parameters:

* prob_Repair: 0.6214
* prob_Mirror: 0.2996
* increase_Repair: 2.6391
* decrease_Mirror: 0.2171
* perc: 0.35

To make an experiment the dataset must be in the same folder and the C++ code for the evolutionary algorithm has to be compiled (both paths can be modified). Then run on the command line:

`python SPOEA.py 200 0 2-10 0 10 3 20 SPO 53162 5 0.6214 0.2996 2.6391 0.2171 0.35`



