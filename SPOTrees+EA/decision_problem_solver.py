'''
Generic file to set up the decision problem (i.e., optimization problem) under consideration
Must have functions: 
  get_num_decisions(): returns number of decision variables (i.e., dimension of cost vector)
  find_opt_decision(): returns for a matrix of cost vectors the corresponding optimal decisions for those cost vectors

This particular file sets up a shortest path decision problem over a 4 x 4 grid network, where driver starts in
southwest corner and tries to find shortest path to northeast corner.
'''

from gurobipy import *
import numpy as np
from ctypes import CDLL, POINTER
from ctypes import c_size_t, c_double
from math import sqrt
import glob

#################### Importing EA writen in C ###################
libfile = glob.glob('/home/felipe/Desktop/SPOTree-EA-2/C_code/ea.so')[0]
mylib = CDLL(libfile)

# C-type corresponding to numpy array
# funcionan como link, y punteros desde python, no liberarlos en C
ND_Pointer_warr = np.ctypeslib.ndpointer(dtype=np.float64,ndim=1,flags="C")
ND_Pointer_res = np.ctypeslib.ndpointer(dtype=np.float64, ndim=1,flags="C")

# Defining prototypes to send data
mylib.ga.argtypes = [ND_Pointer_warr, ND_Pointer_res]

# Represents the result
# The first six elements represents the solution given by the EA
# The last element represents the best evaluation of the best chromosome


############## SPOTree Code ####################
dim = 5 #(creates dim * dim grid, where dim = number of vertices)
popSize = sqrt(dim)*3
R = np.ones((dim-1)*2 + 1)
Edge_list = [(i,i+1) for i in range(1, dim**2 + 1) if i % dim != 0]
Edge_list += [(i, i + dim) for i in range(1, dim**2 + 1) if i <= dim**2 - dim]
Edge_dict = {} #(assigns each edge to a unique integer from 0 to number-of-edges)
for index, edge in enumerate(Edge_list):
    Edge_dict[edge] = index
#print "-" * 20
#print Edge_dict
D = len(Edge_list) # D = number of decisions

Edges = tuplelist(Edge_list)
# Find the optimal total cost for an observation in the context of shortes path
m_shortest_path = Model('shortest_path')
m_shortest_path.Params.OutputFlag = 0
flow = m_shortest_path.addVars(Edges, ub = 1, name = 'flow')
m_shortest_path.addConstrs((quicksum(flow[i,j] for i,j in Edges.select(i,'*')) - quicksum(flow[k, i] for k,i in Edges.select('*',
  i)) == 0 for i in range(2, dim**2)), name = 'inner_nodes')
m_shortest_path.addConstr((quicksum(flow[i,j] for i,j in Edges.select(1, '*')) == 1), name = 'start_node')
m_shortest_path.addConstr((quicksum(flow[i,j] for i,j in Edges.select('*', dim**2)) == 1), name = 'end_node')

def setDimencionAndSeed(d,s,hp1,hp2,inq,deq, newpercTotal):
  # they are globals not from this function
  global dim
  global seed
  global popSize
  global R
  global Edge_list
  global Edge_dict
  global D
  global Edges
  global m_shortest_path
  global flow
  global hc1
  global hc2
  global inqV
  global deqV
  global percTotal
  
  hc1 = hp1
  hc2= hp2
  inqV= inq
  deqV = deq
  percTotal = newpercTotal
  
  dim = d
  seed = s
  popSize = sqrt(dim)*3
  R = np.ones((dim-1)*2 + 1)
  Edge_list = [(i,i+1) for i in range(1, dim**2 + 1) if i % dim != 0]
  Edge_list += [(i, i + dim) for i in range(1, dim**2 + 1) if i <= dim**2 - dim]
  Edge_dict = {} #(assigns each edge to a unique integer from 0 to number-of-edges)
  for index, edge in enumerate(Edge_list):
    Edge_dict[edge] = index
  D = len(Edge_list) # D = number of decisions
  Edges = tuplelist(Edge_list)
  # Find the optimal total cost for an observation in the context of shortes path
  m_shortest_path = Model('shortest_path')
  m_shortest_path.Params.OutputFlag = 0
  flow = m_shortest_path.addVars(Edges, ub = 1, name = 'flow')
  m_shortest_path.addConstrs((quicksum(flow[i,j] for i,j in Edges.select(i,'*')) - quicksum(flow[k, i] for k,i in Edges.select('*',
  i)) == 0 for i in range(2, dim**2)), name = 'inner_nodes')
  m_shortest_path.addConstr((quicksum(flow[i,j] for i,j in Edges.select(1, '*')) == 1), name = 'start_node')
  m_shortest_path.addConstr((quicksum(flow[i,j] for i,j in Edges.select('*', dim**2)) == 1), name = 'end_node')

def get_num_decisions():
  return D
  
def shortest_path(cost):
    # m_shortest_path.setObjective(quicksum(flow[i,j] * cost[Edge_dict[(i,j)]] for i,j in Edges), GRB.MINIMIZE)
    m_shortest_path.setObjective(LinExpr( [ (cost[Edge_dict[(i,j)]],flow[i,j] ) for i,j in Edges]), GRB.MINIMIZE)
    m_shortest_path.optimize()
    return {'weights': m_shortest_path.getAttr('x', flow), 'objective': m_shortest_path.objVal}

def find_opt_decision(cost):
    weights = np.zeros(cost.shape)
    objective = np.zeros(cost.shape[0])
    for l in range(cost.shape[0]):
        R[0] = dim
        R[1] = seed
        R[2] = 5
        R[3] = dim*(dim**percTotal)
        R[4] = hc1
        R[5] = hc2
        R[6] = inqV
        R[7] = deqV
        mylib.ga(cost[l,:], R)
        solution = R[:((dim-1)*2)]
        index = 1
        index2 = 1
        # New form for new representation
        for i in range(len(solution)):
            for j in range(len(solution)):
                if solution[j] == i:
                    if j < len(solution)/2:
                        index2 += dim
                    else:
                        index2 += 1
                    weights[l, Edge_dict[(index,index2)]] = 1
                    index = index2
                    break
        objective[l] = R[-1]
    return {'weights': weights, 'objective':objective}

def shortest_path(cost):
    # m_shortest_path.setObjective(quicksum(flow[i,j] * cost[Edge_dict[(i,j)]] for i,j in Edges), GRB.MINIMIZE)
    m_shortest_path.setObjective(LinExpr( [ (cost[Edge_dict[(i,j)]],flow[i,j] ) for i,j in Edges]), GRB.MINIMIZE)
    m_shortest_path.optimize()
    return {'weights': m_shortest_path.getAttr('x', flow), 'objective': m_shortest_path.objVal}

def find_opt_decision_real(cost):
    weights = np.zeros(cost.shape)
    objective = np.zeros(cost.shape[0])
    for i in range(cost.shape[0]):
        temp = shortest_path(cost[i,:])
        for edge in Edges:
            weights[i, Edge_dict[edge]] = temp['weights'][edge]
        objective[i] = temp['objective']
    return {'weights': weights, 'objective':objective}

