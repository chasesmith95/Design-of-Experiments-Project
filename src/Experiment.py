'''
Created on Jul 2, 2014

@author: vpsmith
'''
from pyDOE import *
from numpy import *
from scipy import *
from scipy.sparse.linalg.isolve import *
import csv

class Experiment(object):
    '''
    classdocs
    '''
    def __init__(self, runTable=None, factorList=None):
        '''
        Constructor
        '''
        self.factorList= factorList
        self.factorHighs=[]
        self.factorLows=[]
        self.runTable= runTable
        self.results=[]
        self.generatorList=[]
        self.numExperiments=[]
        self.factorWeights=[]
        self.factorPVals=[]

    def setNumexperiments(self):
        length=len((self.results)[:,0])
        self.NumExperiments=list([range(length+1)])   
    def addToRunTable(self, Runs):
        self.runTable.union(self.runTable, Runs)
    def getRunTable(self):
        return matrix(self.runTable)
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
class ExperimentOperator(object): 
    def __init__(self):
        self
    def isfloat(self, element):
        try:
            float(element)
            return True
        except ValueError:
            return False
    def createExperimentTable(self, experiment):
        completeMatrix=[0][0]
        factorRow=['Factor Names']
        factorRow.extend(experiment.factorList)
        factorRow.extend(['Result']*len((experiment.results)[0]))
        completeMatrix.append(factorRow)
        
        factorHighRow=['Factor Highs']
        factorHighRow.extend(experiment.factorHighs)
        factorHighRow.extend(['-']*len((experiment.results)[0]))
        completeMatrix.append(factorHighRow)
        
        factorLowRow=['Factor Lows']
        factorLowRow.extend(experiment.factorLows)
        factorLowRow.extend(['-']*len((experiment.results)[0]))
        completeMatrix.append(factorLowRow)
       
        i=0
        while i< len((experiment.runTable)):
            runRow=[str(i)]
            runRow.extend((experiment.runTable)[int(i)])
            runRow.extend((experiment.results)[i])
            completeMatrix.append(runRow)
            i=i+1
        
        
        while i< len((experiment.factorWeights)):
            factorWeightRow=['Factor Weights']
            factorWeightRow.extend((experiment.factorWeights)[i])
            factorWeightRow.extend(['-']*len((experiment.results)[0]))
            completeMatrix.append(factorWeightRow)
            
            factorPValRow=['Factor PVals']
            factorPValRow.extend((experiment.PVals)[i])
            factorPValRow.extend(['-']*len((experiment.results)[0]))
            completeMatrix.append(factorPValRow)
            i=i+1
        return completeMatrix
            
    def writeExperimentToCSV(self, experiment, fName):
        runTable= experiment.runTable
        factorNames= experiment.factorList
        file_name=fName
        with open(file_name, 'w') as csvfile:
            writer = csv.writer(csvfile)
            [writer.writerow(r) for r in (self.createExperimentTable(experiment))]
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
    
    
    
    
    
    
class ExperimentInitializer(ExperimentOperator):
    
    def __init__(self):
        self
    
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
    
  
    def setRunTable(self, experiment, Type=None):
         
        fList=str(experiment.getFactorList()).replace(',', ' ')
        fList.replace('[', '')
        fList.replace(']', '')
        try:
            if(Type=='FF'):
                runTable= fracfact(fList)
            elif(Type=='CCD'):
                runTable= ccdesign(len(fList))
        except ValueError:
            print("Error with input value")
            break
        experiment.addToRunTable(runTable)
           
class ExperimentAnalyzer(ExperimentOperator):
    
    def linearRegression(self, i,  experiment, fName):
        self.readExperimentFromCSV(experiment, fName) 
        runTable= matrix(experiment.runTable)
        experiment.setNumExperiments()
        results=array(experiment.results)[:,i] #this takes one result at a time  
        linearRegressMatrix= lsqr(runTable, results, damp=0.0, atol=1e-6, btol=1e-6, conlim=1e8,
         iter_lim=None, show=False, calc_var=True) 
        experiment.factorWeights.append=linearRegressMatrix[0]
        experiment.factorPVals.append=linearRegressMatrix[(1+len(experiment.numExperiments))]  
        return
    def findSignificantVariables(self, i, experiment):
        #find top variables
        
        return
        
        
        
        
         