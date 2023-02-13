#include <iostream>
#include <vector>
#include <random>
#include <algorithm>
#include <string.h>
using namespace std;

class EvolutionaryAlg {

public:
    int* baseSol;
    //vector<vector<int>> generation;
    int* newGeneration;
    bool* hcCheck;
    //int hc1moves;
    int* bestChromosome;
    int* evChangeHelperReal;
    int* evChangeHelperNew;
    int* movCodes;
    int moveCodesSize;
    float bestQlt;
    float* evFuncWeights;
    float hc1Prob;
    float hc2Prob;
    int totalGenerations;
    int edges;
    int popSize;
    int lenGen;
    int dimension;
    float deqP;
    float inqP;
    mt19937 randGen;
    uniform_real_distribution<double> prob = uniform_real_distribution<>(0.0, 1.0);
    uniform_int_distribution<int> otherIndex;

    EvolutionaryAlg(int nEdges, float* weights, int genSize, float hcEval, float hcNotEval, mt19937 gen, int dim, int totalGen, float inqV, float deqV) : edges(nEdges), evFuncWeights(weights), popSize(genSize), hc1Prob(hcEval), hc2Prob(hcNotEval), randGen(gen), dimension(dim), totalGenerations(totalGen){

        bestQlt = 1000000; //big number
        lenGen = (dimension-1)*2;
        otherIndex = uniform_int_distribution<>(0, (lenGen/2)-1);
        
        // Real decrease and increase, is completly related to the total generations !
	deqP = deqV/totalGenerations;
        inqP = inqV/totalGenerations;
        
	// memory assignation
        newGeneration = (int*)malloc(lenGen*popSize*sizeof(int));
        bestChromosome = (int*)malloc(lenGen*sizeof(int));
        evChangeHelperReal = (int*)malloc(lenGen*sizeof(int));
        evChangeHelperNew = (int*)malloc(lenGen*sizeof(int));
        hcCheck = (bool*)malloc(popSize*sizeof(int));
        baseSol = (int*)malloc(lenGen*sizeof(int));
        moveCodesSize = (lenGen/2 * lenGen/2);
        movCodes = (int*)malloc(moveCodesSize*sizeof(int));
        
        // base solution
        for (int i = 0; i < lenGen; ++i) {
            baseSol[i] = i;
        }
        
        // Create the first generation
        for (int i = 0; i < popSize; ++i) {
            shuffle(baseSol, baseSol + lenGen, randGen);
            memcpy(newGeneration + linearID(i,0), baseSol, lenGen*sizeof(int));
            hcCheck[i] = true;
        }
        
        // Assign the posible moves
        for (int i = 0; i < (lenGen/2 * lenGen/2); ++i) {
            movCodes[i] = i;
        }

    }
    
    // return allways the same ID, based on i and j, so we cach them
    inline int linearID(int i, int j){
    	return i*lenGen+j;
    }
    
    // Free all the allocated memory
    void freeData(){
    	free(newGeneration);
    	free(bestChromosome);
        free(evChangeHelperReal);
    	free(evChangeHelperNew);
    	free(movCodes);
    	free(hcCheck);
    	free(baseSol);
    }

    void print() {
        printf("%d %d %lf %lf\n", edges, popSize, hc1Prob, hc2Prob);
        for (int i = 0; i < edges; ++i) {
            printf("%0.3lf ", evFuncWeights[i]);
        }
        printf("\n");
    }
    
    // Decode the individual, and obtain the quality, by decoding and evaluating
    float evFunc(int chromeIndex) {
        float quality = 0;

        int actualNode = 1;
        int nextNode;
        int weightIndex;
        int actualIndex = linearID(chromeIndex,0);
        
        for (int i = 0; i < lenGen; ++i) {
            int mIndex = newGeneration[actualIndex+ i];
            int current = i < lenGen/2  ? 0 : 1; // up and rigth
            evChangeHelperReal[mIndex] = current;
	}
	
	
	// Once they are decoded, we assign check the diference !!!
	for (int i = 0; i < lenGen; ++i) {
	    if(evChangeHelperReal[i] == 0){ // UP 
	        nextNode = actualNode + dimension;
                weightIndex = actualNode - 1 + edges/2;
	    }
	    else{ // Rigth
	    	nextNode = actualNode + 1;
                weightIndex = actualNode - 1 - actualNode/dimension;
	    }
	    
	    actualNode = nextNode;
            quality += evFuncWeights[weightIndex];
	}
	    
        return quality;
    }

    // Update the best chromosome and quality
    void findBest() {
        float actualQlt;
        int bestID = -1;
        for (int i = 0; i < popSize; ++i) {
            actualQlt = evFunc(i);
            if (actualQlt < bestQlt) {
                bestQlt = actualQlt;
                bestID = i;
            }
        }
	if (bestID != -1){
		memcpy(bestChromosome, newGeneration + linearID(bestID,0), lenGen*sizeof(int));
	}
    }

    void printGen() {
        vector<float> popGen;
        for (int i = 0; i < popSize; ++i) {
            popGen.push_back(evFunc(i));
        }
        cout << *min_element(popGen.begin(), popGen.end()) << endl;
    }

    void printVector(vector<int> ind) {
	    for (int j = 0; j < lenGen; ++j)
	    {
		printf("%d ", ind[j]);
	    }
	    printf("\n");
    }
    
     void printArray(int* ind) {
	    for (int j = 0; j < lenGen; ++j)
	    {
		printf("%d ", ind[j]);
	    }
	    printf("\n");
    }

    void printFullGen(int genNum) {
        printf("Gen %d\n", genNum);
        for (int i = 0; i < popSize; ++i)
        {
            for (int j = 0; j < lenGen; ++j)
            {
                printf("%d ", newGeneration[linearID(i,j)]);
            }
            printf("\n");
        }
    }

    // reinsert the best individual in the last position, with out a care for the quality of this !
    void reinsertBest() {
    	int worstIndex = popSize - 1;
    	memcpy(newGeneration + linearID(worstIndex,0), bestChromosome, lenGen*sizeof(int));
	
    }

    // evolve population
    void evolvePop() {
        for (int i = 0; i < totalGenerations; ++i) {
            //hc1moves = 0;
            for (int index = 0; index < popSize; ++index) {
                if (hcCheck[index]) {
                    // marks as not-modified
                    hcCheck[index] = false;
                    if(prob(randGen) < hc1Prob) {
                        hc1Operator(index);
                    }
                }
            }
            // Saves the best individual before mutation
            findBest();
            for (int index = 0; index < (popSize-1); ++index) {
                if (prob(randGen) < hc2Prob) {
                    int gen = otherIndex(randGen);
                    // mutation modifies individual
                    hcCheck[index] = true;
                    hc2Operator(index, gen);
                }
            }
            
            hc1Prob = hc1Prob - inqP;
            hc2Prob = hc2Prob - deqP;
            
            // Reinsert into te population
            reinsertBest();

        }
    }
    
    // Returns the best !
    int* getBest() const {
        return bestChromosome;
    }

    // repair operator !
    void hc1Operator(int chromeIndex) {
        int first;
        int second;
        float newQlt;
        float actualQlt = evFunc(chromeIndex);
        shuffle(movCodes, movCodes + moveCodesSize, randGen);
        
        for (int index = 0; index < moveCodesSize; ++index) {
            int code = movCodes[index];
            first = code / (lenGen/2);
            second = code % (lenGen/2) + lenGen/2;
            
            swap(newGeneration[linearID(chromeIndex,first)], newGeneration[linearID(chromeIndex,second)]);
            newQlt = evFunc(chromeIndex);
                        
            if (newQlt < actualQlt) {
                // if gets better -> modified
                hcCheck[chromeIndex] = true;
                break;
            } else {
                swap(newGeneration[linearID(chromeIndex,first)], newGeneration[linearID(chromeIndex,second)]);
            }
        }
    }

    // return the best !, but only its value
    float evFuncBest() {
        return bestQlt;
    }
    
    // mirror operator !
    void hc2Operator(int chromeIndex, int genIndex) {
        int second = otherIndex(randGen);

        if (genIndex < lenGen/2) {
            second = second + lenGen/2;
        }
        
        int nToChange = (second - genIndex)/2;

        int genIndexLinear = linearID(chromeIndex,genIndex);
        int secondIndexLinear = linearID(chromeIndex,second);
        
        for(int i = 1; i <= nToChange; ++i) {
            swap(newGeneration[genIndexLinear + i], newGeneration[secondIndexLinear - i]);
        }
        
    }
};

// Settings to be used by the python code, as a .so file
extern "C"
void ga(double *warray, double *rarray) {

    // General settings
    int dim = int(rarray[0]);
    int edges = 2 * dim * dim - 2 * dim;
    int popSize = int(rarray[2]);
    int lenSol = (dim-1) * 2;
    int totGen = int(rarray[3]);
    
    //  hc1 -> chance of aplying the repair move
    //  hc2 -> chance of aplying the mirror move
    //  inq -> General increate (-) in the repair chance (hc1)
    //  deq -> General decrease (+) in the mirror chance (hc2)
    float hc1Prob = float(rarray[4]);
    float hc2Prob  = float(rarray[5]);
    float inq = float(rarray[6]);
    float deq  = float(rarray[7]);
    
    // assign the weights of the moves, in a local value
    float weights[edges];
    int seed = int(rarray[1]);
    static mt19937  gen(seed);
    for (int i = 0; i < edges; ++i) {
        weights[i] = warray[i];
    }

    // call the Evolutionary Algorithm
    EvolutionaryAlg eAlg(edges, weights, popSize, hc1Prob, hc2Prob, gen, dim, totGen,inq, deq );
    eAlg.evolvePop();
    
    // Obtain the best solution
    int* solution = eAlg.getBest();

    // save the best individual to be returned !
    for (int i = 0; i < lenSol; ++i) {
        rarray[i] = solution[i];
    }
    
    // save the best solution value
    rarray[lenSol] = eAlg.evFuncBest();
    
    // finally free the memory allocation
    eAlg.freeData();
}

int main() {

    return 0;
}
