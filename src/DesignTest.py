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


