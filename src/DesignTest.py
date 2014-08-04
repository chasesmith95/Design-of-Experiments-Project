'''
Created on Jul 2, 2014

@author: vpsmith
'''
from pyDOE import *

import csv
from scipy.sparse.linalg.isolve import *
import numpy as np
from sklearn.externals import six
import matplotlib.pyplot as plt


fract= (fracfact('a b c ab ac cb abc'))
# print(fract)

results =str("1.75 3.5 2.45 5.25 32.2 76.3 26.6 177.1 0.35 10.5 1.05 8.05 44.8 121.1 73.5 156.1 11.9 39.2 25.2 92.4 44.1 113.4 72.1 103.6 20.3 30.8 23.8 60.2 87.5 151.9 58.8 179.2 218.4,0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.01 0.00 0.01 0.00 0.07 0.00 0.00 0.12 0.07 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.01 0.00 0.16 0.08 0.00 0.00 0.07 0.05 0.01,0.1 0.3 0.2 0.1 0.3 0.6 2.2 1.1 0.0 0.0 4.0 1.3 7.9 0.8 4.9 7.7 0.9 0.3 1.1 4.5 0.7 0.1 0.5 1.3 0.6 1.0 5.7 7.3 1.1 1.8 4.5 3.3,94.5 61.7 94.4 77.9 68.5 51.4 62.2 48.4 67.5 86.6 80.6 92.4 72.9 35.0 66.6 37.1 65.1 59.3 53.6 55.2 51.7 42.0 51.5 33.4 65.9 38.3 49.7 37.8 49.7 35.8 36.2 34.9")
results=list(results.split(','))
results[0]=list(results[0].split(' '))
results[1]=list(results[1].split(' '))
results[2]=list(results[2].split(' '))
results[3]=list(results[3].split(' '))
results1="0.12     0.85     1.59     4.55     0.46     0.46     1.60     1.74     1.25     0.51     1.49     0.52     3.63     0.60     2.25     3.64     0.88     0.36     1.31     2.54     0.40     0.17     0.43     1.00     0.36     0.50     2.25     3.23     0.58     0.94     1.87     1.28     1.39 ,0.12     0.09     0.00     0.06     0.05     0.04     0.27     0.12     0.00     0.04     0.00     0.01     0.54     0.04     0.48     0.34     0.07     0.02     0.12     0.26     0.14     0.05     0.07     0.11     0.11     0.07     0.31     0.38     0.13     0.18     0.67     0.31     0.31 ,27.30     3.02     26.20     9.44     4.43     3.77     5.89     5.96     2.50     7.44     11.40     7.70     10.20     1.81     11.20     8.37     12.00     7.94     10.90     12.90     4.53     3.00     6.85     5.94     12.80     3.40     18.00     11.90     3.69     3.01     5.65     5.63     8.32,0.269230769    0.538461538    0.376923077    0.807692308    4.953846154    11.73846154    4.092307692    27.24615385    0.053846154    1.615384615    0.161538462    1.238461538    6.892307692    18.63076923    11.30769231    24.01538462    1.830769231    6.030769231    3.876923077    14.21538462    6.784615385    17.44615385    11.09230769    15.93846154    3.123076923    4.738461538    3.661538462    9.261538462    13.46153846    23.36923077    9.046153846    27.56923077    33.6,0.00    0.00    0.0    0.0    0.0    14.2681    4.9476    113.344    0.0    11.34    0.0    59.1675    0.0    44.4437    882    1102.066    0.0    0.0    0.0    24.024    11.4219    0.0    0.0    39.1608    11.8146    0.0    371.28    454.51    0.0    27.4939    423.36    922.88"
results1=list(results1.split(','))
i=0
while i<len(results1):
    result=str(results1[i])
    result=result.replace('     ', ' ')
    result=list(result.split(' '))
    results.append(result)
    #print("This is the array " + str(result))
    i=i+1
#experimentOp=ExperimentOperator()
i=0
while i<len(results):
    j=0
    while j<len(results[i]):
        if(results[i][j]==''):
            results[i].pop(j)
        else:
            result=int(float(str(results[i][j]))*100)
            if(i==0):
                result=float(result/50)
            if(i==8):
               result=float(result/1000)
            results[i][j]=result
            j=j+1
    print("This is the end result" + str(results[i]))
    print(len(results[i]))
    i=i+1
    
#experimentOp=ExperimentOperator()
#experiment = Experiment()        
#experimentOp.readExperimentFromCSV(experiment, r"C:\Users\vpsmith\Documents\New folder (3)\Experiment1-2 LevelFractionalFactorial.csv") 
#experimentOp.graphExperimentDistribution(experiment)
#print(experiment.results)
#print(experiment.runTable)
i=0
#while( i<(len(experiment.results))):

       
   # experimentOp.linearRegression(i, experiment)
   # print(i)
   # i=i+1
   # except:
        #experimentOp.writeExperimentToCSV(experiment, r'C:/Users/vpsmith/My Documents/Experiment1FractionalFactorial.csv')
    #    i=i+1


#experimentOp.findSignificantVariables(0, experiment)
#experimentOp.linearRegression(1, experiment)
#experimentOp.findSignificantVariables(1, experiment)
#experimentOp.linearRegression(2, experiment)
#experimentOp.findSignificantVariables(2, experiment)
#experimentOp.linearRegression(3, experiment)
#experimentOp.findSignificantVariables(3, experiment)
#experimentOp.writeExperimentToCSV(experiment, r"C:/Users/vpsmith/My Documents/Experiment1-2 Level Fractional Factorial.csv")


def graphExperimentDistribution(self, experiment):
    experiments=experiment.numExperiments
    numExperiments= len(experiments)+1
    results= experiment.results
    plt.figure(1)
    i=0
    while i<len(results):
        subplotInit(plot=plt, subplotNumber=i, subplotXLabel=None, subplotYLabel=None, subplotTitle=None, numExperiments=numExperiments, experiments=experiments, results=results[i]) 
        i=i+1   
    plt.show()
    
    
def subplotInit(plot=plt, subplotRows=2, subplotColumns=1, subplotNumber=1, subplotXLabel=None, subplotYLabel=None, subplotTitle=None, numExperiments=9, experiments=None, results=None):
    plt.subplot(subplotRows,subplotColumns,subplotNumber)
    plt.axis([0, numExperiments, 0 ,1])
    plt.autoscale(enable=True, axis='y', tight=None)
    plt.plot(experiments, results, 'ro')
    plt.xlabel(subplotXLabel)
    plt.ylabel(subplotYLabel)
    plt.title(subplotTitle)
    plt.tight_layout()
    plt.grid(True)




def isfloat(element):
    try:
        float(element)
        return True
    except ValueError:
        return False
    
    
#regressionMatrix= lsqr(fract, numpy.array(answer), damp=0.0, atol=1e-8, btol=1e-8, conlim=1e8, iter_lim=None, show=False, calc_var=True)

# print(regressionMatrix[0])
#numpy.array=['SCF', 'FL', 'GM','SRI', 'IL-3', 'IL-6', 'Noparin', 'TPO', 'IL-11']
#answers=regressionMatrix[0]
#variance=regressionMatrix[9]
#print(variance)

experiments=list(range(9))
experiments=experiments[1:]
answer=[20, 35, 7, 42, 36, 50, 45, 82]
plt.figure(1)
subplotInit(plt, 2,1,1, 'Experiment Number', 'Percent of XDC Cells', 'Distribution of Percent of XDC Cells', numExperiments=8, experiments=experiments, results=answer)
subplotInit(plt, 2,1,2, 'Experiment Number', 'Percent of XDC Cells', 'Distribution of Percent of XDC Cells', numExperiments=8, experiments=experiments, results=answer)
plt.show()


