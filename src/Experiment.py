'''
Created on Jul 2, 2014

@author: vpsmith
'''
from pyDOE import *
from numpy import *
import numpy as np
from scipy import *
from scipy.sparse.linalg.isolve import *
import csv
from sklearn.externals import six
import matplotlib.pyplot as plt

class Experiment(object):
    '''
    classdocs
    '''
    def __init__(self, runTable=[], factorList=[], factorHighs=[], factorLows=[], results=[], generatorList='', numExperiments=[], factorWeights=[], factorPvals=[] ):
        '''
        Constructor
        '''
        self.factorList= factorList
        self.factorHighs=factorHighs
        self.factorLows=factorLows
        self.runTable= runTable
        self.results=results
        self.generatorList=generatorList
        self.numExperiments=[]
        self.factorWeights=factorWeights
        self.factorPVals=factorPvals
        self.independentList=["Total Number of Cells (X100)", "Percent of D141 + C9a+(/10000)", "Percentage of CD1c(/10000)", "Percentage of PTK7 (/10000)" ]

    def setNumExperiments(self):
        length=len(matrix(self.runTable)[:,0])
        self.numExperiments=list(range(length+1))[1:]   
    def addToRunTable(self, Runs):
        self.runTable= doe_union.union(matrix(self.runTable), matrix(Runs))
    def setRunTable(self, runTable):
        self.runTable= runTable
    def getRunTable(self):
        return list(self.runTable)
    def getFactorList(self):
        return list(self.factorList) 
    def setFactorList(self, factorList):
        self.factorList= factorList
    def setResults(self, results):
        self.results=results
    def setFactorLows(self, factorLows):
        self.factorLows=factorLows
    def setFactorHighs(self, factorHighs):
        self.factorHighs=factorHighs
    def setFactorPVals(self, pVals):
        self.factorPVals=pVals
    def setFactorWeights(self, factorWeights):
        self.factorWeights=factorWeights
    
 #base class for experiment manipulators
class ExperimentOperator: 
    def __init__(self):
        self
    def isfloat(self, element):
        try:
            float(element)
            return True
        except ValueError:
            return False
    def createExperimentTable(self, experiment):
        completeMatrix=[]
        factorRow=['Factor Names']
        #print(len(experiment.results))
        factorRow.extend(list(experiment.factorList))
        i=0
        while i < len(experiment.results): 
            factorRow.append("Results: " + str(experiment.independentList[i]))
            i=i+1
        completeMatrix.append(list(factorRow))
        
        factorHighRow=['Factor Highs']
        factorHighRow.extend(experiment.factorHighs)
        factorHighRow.extend(list(['-']*len((experiment.results))))
        completeMatrix.append(factorHighRow)
        
        factorLowRow=['Factor Lows']
        factorLowRow.extend(experiment.factorLows)
        factorLowRow.extend(list(['-']*len((experiment.results))))
        completeMatrix.append(factorLowRow)
       
        i=0
        while i < len(list(experiment.runTable)):
            runRow=[str(i)]
            runTableRow=str(list(experiment.runTable)[int(i)])
            runTableRow=runTableRow.replace('matrix', '')
            runTableRow=runTableRow.replace(']','')
            runTableRow=runTableRow.replace('[','') 
            #runTableRow=runTableRow.replace('.','')
            runTableRow=runTableRow.replace(',', '')
            runTableRow=runTableRow.replace('  ',',')
            runTableRow=runTableRow.replace('-',',-')
            runTableRow=list(runTableRow.split(','))
            #print(runTableRow)
            if(runTableRow[0]==''):
                runTableRow=runTableRow[1:]
            runRow.extend(runTableRow)
            #print(runRow)
        
            for num in (list(experiment.results)):
                #print(list(num))
                runRow.append(list(num)[i])
            
            #print(runRow)
            completeMatrix.append(list(runRow))
            i=i+1
        
        i=0
        j=i+1
        while i< len((experiment.factorWeights)):
            factorWeightRow=['Factor Weights ' + str(experiment.independentList[i])]
            factorWeightRow.extend(list(experiment.factorWeights)[i])
            #print(factorWeightRow)
            factorWeightRow.extend(list(['-']*len((experiment.results))))
            completeMatrix.append(list(factorWeightRow))
            
            factorPValRow=['Factor PVals ' + str(experiment.independentList[i])]
            factorPValRow.extend(list(experiment.factorPVals)[i])
            factorPValRow.extend(list(['-']*len((experiment.results))))
            completeMatrix.append(list(factorPValRow))
            i=i+1
        return completeMatrix
            
    def writeExperimentToCSV(self, experiment, fName):
        file_name=fName
        with open(str(file_name), 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)
            for r in ((self.createExperimentTable(experiment))):
                writer.writerow(r)
            
        return
    def readExperimentFromCSV(self, experiment, fName):
        file_name=fName
        with open(file_name, 'r') as csvfile:
            fileReader = csv.reader(csvfile)
            end=0
            for row in fileReader:
                i=0
                j=i+1
                while i<len(row):
                    if(row[i]=='Factor Names'):
                        end=row.index('Results')
                        experiment.factorList= row[j:end]
                    elif(row[i]=='Factor Highs'):
                        self.factorHighs= row[j:end]
                    elif(row[i]=='Factor Lows'):
                        self.factorLows= row[j:end]
                    elif(self.isfloat(row[i])==True and (i<end and i>0) ):
                        self.runTable.extend= row[j:end] 
                    elif(row[i]=='Factor Weights'):
                        self.factorWeights= row[j:end]
                    elif(row[i]=='Factor PValues'):
                        self.factorPVals= row[j:end] 
                    elif(i==end and self.isfloat(row[i])==True):
                        self.results.append = row[i:len(row)]
                    i=i+1
        return
    def setRunTableHighLow(self, experiment):
        i=0
        runTable= experiment.getRunTable()
        while(i< len(runTable)):
            j=0
            while(j<len(runTable[i])): 
                if(int(runTable[i][j])==-1):
                    runTable[i][j]='-'
                elif(int(runTable[i][j])==1):
                    runTable[i][j]='+'
                j=j+1
            i=i+1
        return runTable
    
  
    def setRunTable(self, experiment, Type='FF'):
         
        fList=str(experiment.generatorList)
        print(fList)
        try:
            if(Type=='FF'):
                runTable= matrix(fracfact(fList))
            elif(Type=='CCD'):
                runTable= ccdesign(len(fList))
        except ValueError:
            print("Error with input value")
            return
        experiment.setRunTable(runTable)
    
    def linearRegression(self, k,  experiment, fName=None):
        i=k
        if(fName==None):
            runTable= matrix(experiment.runTable)
            experiment.setNumExperiments()
            results=np.array((experiment.results)[i][0:32]) #this takes one result at a time  
            linearRegressMatrix= lsqr(np.matrix(runTable), np.array(results), damp=0.0, atol=1e-6, btol=1e-6, conlim=1e8,
             iter_lim=None, show=False, calc_var=True) 
            #print(linearRegressMatrix[0])
            #print(linearRegressMatrix[(len(experiment.factorList))])
            factorWeight=list(linearRegressMatrix[0])
            factorPVals=list(linearRegressMatrix[(len(experiment.factorList))] )
            experiment.factorWeights.append(factorWeight)
            experiment.factorPVals.append(factorPVals)  
            return
        elif(fName!=None):
            self.readExperimentFromCSV(experiment, fName) 
            runTable= matrix(experiment.runTable)
            experiment.setNumExperiments()
            results=list((experiment.results)[i]) #this takes one result at a time  
            linearRegressMatrix= lsqr(runTable, np.array(results), damp=0.0, atol=1e-6, btol=1e-6, conlim=1e8,
             iter_lim=None, show=False, calc_var=True) 
            experiment.factorWeights.append=linearRegressMatrix[0]
            #print(linearRegressMatrix[0])
            #print(linearRegressMatrix[(1+len(experiment.numExperiments))])
            experiment.factorPVals.append=linearRegressMatrix[(1+len(experiment.numExperiments))]  
            return
    def findSignificantVariables(self, j, experiment):
        #find top variables
        sigFactors=list(experiment.factorWeights[j])
        sigFactors.sort(reverse=True)
        sigFactors=sigFactors[0:5]
        i=0
        while i < len(sigFactors):
            facNameInd=(experiment.factorWeights[j]).index(sigFactors[i])
            sigF=list(str(sigFactors[i]))
            sigF.append(experiment)
        
        print(sigFactors)
        return
    def graphExperimentDistribution(self, experiment):
        experiment.setNumExperiments()
        experiments=list(experiment.numExperiments)
        numExperiments= len(experiments)+1
        #print(experiments)
       
        results= list(experiment.results)
        print(len(results[2]))
        plt.figure(1)
        i=0
        while i<len(results):
            self.subplotInit(plot=plt, subplotRows=2, subplotColumns=int(len(experiment.results)/2) ,subplotNumber=i, subplotXLabel="Experiment Number", subplotYLabel=experiment.independentList[i], subplotTitle="Experiment 1", numExperiments=numExperiments, experiments=experiments, results=results[i][0:32]) 
            i=i+1   
        plt.show()
    
    
    def subplotInit(self, plot=plt, subplotRows=2, subplotColumns=1, subplotNumber=1, subplotXLabel=None, subplotYLabel=None, subplotTitle=None, numExperiments=9, experiments=None, results=None):
        plt.subplot(subplotRows,subplotColumns,subplotNumber)
        plt.axis([0, numExperiments, -1 ,1])
        plt.autoscale(enable=True, axis='y', tight=None)
        plt.plot(experiments, results, 'ro')
        plt.xlabel(subplotXLabel)
        plt.ylabel(subplotYLabel)
        plt.title(subplotTitle)
        plt.tight_layout()
        plt.grid(True)

'''
independentList=["Total Number of Cells (X10)", "Percent of D141 + C9a+"]
results =str("1.75 3.5 2.45 5.25 32.2 76.3 26.6 177.1 0.35 10.5 1.05 8.05 44.8 121.1 73.5 156.1 11.9 39.2 25.2 92.4 44.1 113.4 72.1 103.6 20.3 30.8 23.8 60.2 87.5 151.9 58.8 179.2 218.4,0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.01 0.00 0.01 0.00 0.07 0.00 0.00 0.12 0.07 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.01 0.00 0.16 0.08 0.00 0.00 0.07 0.05 0.01,0.1 0.3 0.2 0.1 0.3 0.6 2.2 1.1 0.0 0.0 4.0 1.3 7.9 0.8 4.9 7.7 0.9 0.3 1.1 4.5 0.7 0.1 0.5 1.3 0.6 1.0 5.7 7.3 1.1 1.8 4.5 3.3,94.5 61.7 94.4 77.9 68.5 51.4 62.2 48.4 67.5 86.6 80.6 92.4 72.9 35.0 66.6 37.1 65.1 59.3 53.6 55.2 51.7 42.0 51.5 33.4 65.9 38.3 49.7 37.8 49.7 35.8 36.2 34.9")
results=list(results.split(','))
results[0]=list(results[0].split(' '))
results[1]=list(results[1].split(' '))
results[2]=list(results[2].split(' '))
results[3]=list(results[3].split(' '))
i=0
while i<len(results):
    j=0
    while j<len(results[i]):
        results[i][j]=int(float(results[i][j])*100)
        j=j+1
    i=i+1
experiment = Experiment(factorList=['SCF','FL','GM','SRI','IL-3','IL-6','Noparin','TPO','IL-11'], factorLows=[0,0,0,0,0,0,0,0,0], factorHighs=[100,100,100,100,100,100,100,100,100], results=results, generatorList='a b c d e bcde acde abde abce' )        
experimentOp=ExperimentOperator()
experimentOp.setRunTable(experiment) 
experimentOp.graphExperimentDistribution(experiment)
experimentOp.linearRegression(0, experiment)
#experimentOp.findSignificantVariables(0, experiment)
experimentOp.linearRegression(1, experiment)
#experimentOp.findSignificantVariables(1, experiment)
experimentOp.linearRegression(2, experiment)
#experimentOp.findSignificantVariables(2, experiment)
experimentOp.linearRegression(3, experiment)
#experimentOp.findSignificantVariables(3, experiment)
experimentOp.writeExperimentToCSV(experiment, 'C:/Users/vpsmith/My Documents/Experiment1FractionalFactorial.csv')
        
         '''