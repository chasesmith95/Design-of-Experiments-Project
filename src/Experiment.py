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
#independentList=["Total Number of Cells (X100)", "Percent of D141 + C9a+(/100)", "Percentage of CD1c(/100)", "Percentage of PTK7 (/100)", "CD14+%(/100)", "CD141dim CLEC9A+%(/100)",  "CD141+%(/100)", "Fold", "Number of XDC(/100)"  ]

        

class Experiment(object):
    '''
    classdocs
    '''
    def __init__(self, runTable=[], factorList=[], fixedVariables=[], factorHighs=[], factorLows=[], results=[], generatorList='', numExperiments=[], factorWeights=[], factorPvals=[], independentVariableList=[] ):
        '''
        Constructor
        '''
        self.factorList= factorList
        self.factorHighs=factorHighs
        self.factorLows=factorLows
        self.runTable= runTable
        self.results=results
        self.fixedVariables=fixedVariables
        self.generatorList=generatorList
        self.numExperiments=[]
        self.factorNum=len(self.factorList)
        self.factorWeights=factorWeights
        self.factorPVals=factorPvals
        self.independentVariableList=independentVariableList

    def setNumExperiments(self):
        length=len(np.matrix(self.runTable)[:,0])
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
        factorRow=(experiment.factorList)
        factorRow.extend(experiment.fixedVariables)
        if(experiment.factorList[0]!='Factor Names'):
            factorRow.insert(0, 'Factor Names')
        
       
        
        #print(len(experiment.results))
       
        if(len(experiment.results)>0):
            i=0
            while( i < len(experiment.results)): 
                factorRow.append("Results: " + str((experiment.independentVariableList[i])))
                i=i+1
        completeMatrix.append(list(factorRow))
        factorHighRow=experiment.factorHighs
        if(experiment.factorHighs[0]!='Factor Highs'):
            factorHighRow.insert(0, 'Factor Highs')
        
        
        
        if(len(experiment.results)>0):
            factorHighRow.extend(list(['-']*len((experiment.results))))
        completeMatrix.append(factorHighRow)
        factorLowRow=experiment.factorLows
        if(experiment.factorLows[0]!='Factor Lows'):
            factorLowRow.insert(0,'Factor Lows')
        
        if(len(experiment.results)>0):
            factorLowRow.extend(list(['-']*len((experiment.results))))
       
        completeMatrix.append(factorLowRow)
       
        i=0
        j=i+1
        while i < len(list(experiment.runTable)):
            runRow=[str(j)]
            runTableRow=str(list(experiment.runTable)[int(i)])
            runTableRow=runTableRow.replace('matrix', '')
            runTableRow=runTableRow.replace(']','')
            runTableRow=runTableRow.replace('[','') 
            #runTableRow=runTableRow.replace('.','')
            runTableRow=runTableRow.replace(',', '')
            runTableRow=runTableRow.replace('  ',',')
            runTableRow=runTableRow.replace('-',',-')
            runTableRow=list(runTableRow.split(','))
            runTableRow.extend(list(['1.']*len(experiment.fixedVariables)))
            print(runTableRow)
            k=0
            while k<len(runTableRow):
                if(runTableRow[k]=='' or runTableRow[k]==' '):
                    runTableRow.pop(k)
                    k=0
                elif(runTableRow[k]!=''):
                    k=k+1
            
            runRow.extend(runTableRow)
            #print(runRow)
            if(len(experiment.results)>0):
                for num in (list(experiment.results)):
                    #print(list(num))
                    runRow.append(list(num)[i])
                
                #print(runRow)
            completeMatrix.append(list(runRow))
            i=i+1
            j=j+1
        if(len(experiment.factorWeights)>0):
            i=0
            j=i+1
            while i< len((experiment.factorWeights)):
                factorWeightRow=['Factor Weights ' + str(experiment.independentVariableList[i])]
                factorWeightRow.extend(experiment.factorWeights[i])
                #print(factorWeightRow)
                factorWeightRow.extend(list(['-']*len((experiment.results))))
                completeMatrix.append(list(factorWeightRow))
                
                factorPValRow=['Factor PVals ' + str(experiment.independentVariableList[i])]
                factorPValRow.extend(experiment.factorPVals[i])
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
        experiment.runTable=list()
        experiment.results=list()
        with open(file_name, 'r') as csvfile:
            fileReader = csv.reader(csvfile)
            end=0
            for row in fileReader:
                i=0
                j=i+1
                while i<len(row):
                    if(row[i]=='Factor Names'):
                        k=0
                        while k<len(row):
                            if(row[k].find('Results')>=0):
                                end=k
                                print(end)
                                break
                            else:
                                k=k+1
                        experiment.factorList= row[j:end]
                    elif(row[i]=='Factor Highs'):
                        experiment.factorHighs= row[j:end]
                    elif(row[i]=='Factor Lows'):
                        experiment.factorLows= row[j:end]
                    elif((self.isfloat(row[i]))==True and i==0):
                            runTab=((row[j:end]))
                            experiment.runTable.append(runTab)
                    elif((row[i]).count('Factor Weights')>0):
                        experiment.factorWeights.append(row[j:end])
                    elif((row[i]).count('Factor PValues')>0):
                        experiment.factorPVals.append(row[j:end]) 
                    elif(i==end and self.isfloat(row[i])==True):
                        experiment.results.append(list(row[i:len(row)]))
                        
                    if(i==end and self.isfloat(row[i])==False and len(experiment.independentVariableList)<1):
                        experiment.independentVariableList=(row[i:len(row)])
                        n=0
                        while( n<len(experiment.independentVariableList)):
                            experiment.independentVariableList[n]=(experiment.independentVariableList[n]).replace('Results: ','')
                            n=n+1
                    j=j+1
                    i=i+1
                    
        experiment.results=  (np.array(list(zip(*list(experiment.results)))))
        experiment.runTable= np.asmatrix(experiment.runTable, float)
            
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
        fNum=int(experiment.factorNum)
        print(fList)
        try:
            if(Type=='FF'):
                runTable= matrix(fracfact(fList))
            elif(Type=='CCD'):
                runTable= ccdesign(int(fNum), generatorList= experiment.generatorList,center=(0, 3), alpha='rotatable')
        except ValueError:
            print("Error with input value")
            return
        experiment.setRunTable(runTable)
    
    def linearRegression(self, k,  experiment, fName=None):
        i=k
        if(fName==None):
            runTable= np.asmatrix(experiment.runTable, float)
            experiment.setNumExperiments()
            results=np.array((experiment.results)[i])
            results=results.astype(np.float) #this takes one result at a time  
            
            linearRegressMatrix= lsqr(np.matrix(runTable), np.array(results), damp=0.0, atol=0, btol=0, conlim=0,
             iter_lim=None, show=False, calc_var=True) 
            print(linearRegressMatrix)
            print(linearRegressMatrix[0])
            #print(linearRegressMatrix[(len(experiment.factorList))])
            factorWeight=list(linearRegressMatrix[0])
            #factorPVals=list(linearRegressMatrix[(len(experiment.factorList))] )
            experiment.factorWeights.append(factorWeight)
            #experiment.factorPVals.append(factorPVals) 
            experiment.factorPVals.append((['0']*len(linearRegressMatrix[0]))) 
            experiment.runTable=np.matrix(runTable)
            return
        elif(fName!=None):
            self.readExperimentFromCSV(experiment, fName) 
            runTable= np.matrix(experiment.runTable)
            experiment.setNumExperiments()
            results=np.array(((experiment.results)[i])) #this takes one result at a time  
            linearRegressMatrix= lsqr(matrix(runTable), (results), damp=0.0, atol=0, btol=0, conlim=0,
             iter_lim=None, show=False, calc_var=True) 
            print(linearRegressMatrix[0])
            print(linearRegressMatrix[(len(experiment.factorList))])
            experiment.factorWeights.append=linearRegressMatrix[0]
            #print(linearRegressMatrix[0])
            #print(linearRegressMatrix[(1+len(experiment.numExperiments))])
            experiment.factorPVals.append(linearRegressMatrix[(['0']*len(linearRegressMatrix[0]))])  
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
        results= (experiment.results)
        print(results)
        print(len(results))
        i=0
        f=1
        while i<len(results):
            j=1
            plt.figure(f)
            while (j<=1):
                self.subplotInit(plot=plt, subplotRows=1, subplotColumns=1 ,subplotNumber=j, subplotXLabel="Experiment Number", subplotYLabel=experiment.independentVariableList[i], subplotTitle="Experiment 1", numExperiments=numExperiments, experiments=experiments, results=results[i])
                j=j+1 
                i=i+1   
            f=f+1
        plt.show()
    def graphExperimentFactorSignificance(self,experiment):
        experiments=list(experiment.factorList)
        results=list(experiment.factorWeights)
        results= results
        #N = len(results)
        #fig, ax = plt.subplots()
        #print(N)
        print(results)
        N=len(results)
        ind = np.arange(N)  # the x locations for the groups
        width = 0.45       # the width of the bars
       
        i=0
        j=1
        
        
        while i<len(results):
            graph=list(map(float,results[i]))
            
            fig, ax=plt.subplots()
            ax.bar(ind, graph, width, color='y')  
            ax.set_ylabel('Factor Significance')
            ax.set_title("Factor Significance of " + experiment.independentVariableList[i])
            ax.set_xticks(ind+width)
            ax.set_xticklabels( experiment.factorList )
            plt.figure(j)
           
            i=i+1
            j=j+1
        # add some
        
       
        #ax.legend( , (experiments) )
        
        plt.show()
        
    
    def subplotInit(self, plot=plt, subplotRows=2, subplotColumns=1, subplotNumber=1, subplotXLabel=None, subplotYLabel=None, subplotTitle=None, numExperiments=9, experiments=None, results=None):
        plt.subplot(subplotRows,subplotColumns,subplotNumber)
        results=np.array(results)
        results=results.astype(np.float)
        average=np.average(results)
        plt.axis([0, numExperiments, -1 ,1])
        plt.autoscale(enable=True, axis='y', tight=None)
        plt.plot(experiments, results, 'ro')
        plt.plot(experiments, list([average]*len(experiments)), 'b')
        plt.xlabel(subplotXLabel)
        plt.ylabel(subplotYLabel)
        plt.title(subplotTitle)
        plt.tight_layout()
        plt.grid(True)

