import numpy as np
import pickle
import sys
						
def genFeatVectors(nfeat, nvectors):
	featVectors = np.empty((0, nfeat))
	for i in range(nvectors):
		newVec = np.array([np.random.uniform(0, 1,nfeat)]) # SPOT
		#newVec = np.array([np.random.normal(0, 1, nfeat)]) # Original
		featVectors = np.concatenate((featVectors, newVec))
	return featVectors

def genBMatrix(nFeat, nEdges):
	bMatrix = np.empty((0, nEdges))
	for i in range(nFeat):
		featProb = np.array([np.random.binomial(1, 0.5, nEdges)])
		bMatrix = np.concatenate((bMatrix, featProb))
	return bMatrix

def genCostVector(featVector, bMatrix, noise, degree, nEdges, nFeatures):
	noiseTerms = np.random.uniform(1-noise, 1+noise, nEdges)
	costEdges = np.zeros(nEdges)
	for i in range(nEdges):
		costEdge = (1 / np.sqrt(nFeatures) * (sum(bMatrix[:, i] * featVector)) + 1) ** degree * noiseTerms[i]
		costEdges[i] = costEdge
	return np.array([costEdges])

def genVectors(nFeatures, nEdges, nTrain, nTest, noise, degree):
	featVectorsTrain = genFeatVectors(nFeatures, nTrain)
	bMatrix = genBMatrix(nFeatures, nEdges)
	costVectorsTrain = np.empty((0, nEdges))
	for fVec in featVectorsTrain:
		costVec = genCostVector(fVec, bMatrix, noise, degree, nEdges, nFeatures)
		costVectorsTrain = np.concatenate((costVectorsTrain, costVec))
	featVectorsTest = genFeatVectors(nFeatures, nTest)
	costVectorsTest = np.empty((0, nEdges))
	for fVec in featVectorsTest:
		costVec = genCostVector(fVec, bMatrix, noise, degree, nEdges, nFeatures)
		costVectorsTest = np.concatenate((costVectorsTest, costVec))
	return [featVectorsTrain, costVectorsTrain, featVectorsTest, costVectorsTest]


np.random.seed(2022)

nFeatures = 5
dim = int(sys.argv[1])
nEdges = 2 * dim * dim - 2 * dim
nTrain= 200
nTest = 1000
noiseTerms = [0, 0.25, 0.5]
degreeTerms = [2, 10]
numDatasets = 10

data = dict()
data[nTrain] = dict()

for degree in degreeTerms:
	data[nTrain][degree] = dict()
	for noise in noiseTerms:
		data[nTrain][degree][noise] = []
		for i in range(numDatasets):
			dataset = genVectors(nFeatures, nEdges, nTrain, nTest, noise, degree)
			data[nTrain][degree][noise].append(dataset)

with open("non_linear_data_dim" + str(dim) + ".p", "wb") as handle:
	pickle.dump(data, handle, protocol = pickle.HIGHEST_PROTOCOL)

