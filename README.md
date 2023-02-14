# SPOTrees + EA

Code base of the paper "Decision Trees+Evolutionary Algorithm for Predict then Optimize". 

The algorithms are implemented in C++ and Python 2.7, using the following packages: numpy, pandas, scipy, joblib and gurobipy (with a valid Gurobi license).

#### Folder content:

* SPOTrees Original: Code base from the original work on which our implementation is based. Required to retrieve the results from SPO and CART (Full implementation available on https://github.com/rtm2130/SPOTree).

* SPOTrees+EA: Integration of the evolutionary algorithm to the framework. Requiered to retrieve the results from SPO+EA.

* C_code: Implementation of the evolutionary algorithm in C++. Used to solve an instance of the Shortest Path Problem. 

* Dataset: Code to generate the datasets used and to select the seeds for the evolutionary algorithm.