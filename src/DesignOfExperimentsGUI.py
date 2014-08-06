'''
Created on Jul 10, 2014

@author: vpsmith
'''
from tkinter import *
from tkinter import ttk
from Experiment import Experiment, ExperimentOperator
class MainDialog(ttk.tkinter.Tk):
    def __init__(self):
        ttk.tkinter.Tk.__init__(self)
        
        self.title("Design of Experiments")
        self.loadExperiment=StringVar()
        self.folderName=StringVar()
        self.experimentName=StringVar()
        self.experimentType=StringVar()
        self.listFactors= StringVar()
        self.listFixedFactors=StringVar()
        self.listResults= StringVar()
        self.factorLows=StringVar()
        self.factorHighs=StringVar()
        self.numFactors=StringVar()
        self.factorGenerator=StringVar()
        self.listSignificantFactors=[]
        self.listFactorWeights=[]
        self.fracFactRunList=["5 Factor Design(16 Runs and Resolution V)","6 Factor Design(16 Runs and Resolution IV)", "9 Factor Design (32 Runs and Resolution IV)"]
        self.centralCompositeDesignGeneratorDict={5:'a b c d abcd'}
        self.fractFactGeneratorDict = {("5 Factor Design(16 Runs and Resolution V)"):'a b c d abcd',"6 Factor Design(16 Runs and Resolution IV)":'a b c d abc bcd', "9 Factor Design (32 Runs and Resolution IV)": 'a b c d e bcde acde abde abce'}
        
        self.experiment=Experiment()
        self.graphList=["Distribution", "Factor Significance"]
        self.graphType=StringVar()
        
        self.fitList=["Linear Regression"]
        self.fitType=StringVar()
        self.createExperimentFrame= ttk.Frame(self)
        self.initExperimentFrame= ttk.Frame(self)
        self.makeCreateExperimentFrame(Shown=True)
        
       

    def makeCreateExperimentFrame(self, Shown=False):
        if(Shown==True):
            self.title("Design of Experiments: Create Experiment")
            self.geometry("600x200+350+350")
            Label(self.createExperimentFrame, text="Choose Configuration: ", font=(12)).grid(column=2, row=3, padx=10, pady=10)
            self.createExperimentFrame.experimentBox = ttk.Combobox(self.createExperimentFrame, textvariable=self.loadExperiment)
            self.createExperimentFrame.experimentBox['values'] = ['Create New Experiment', 'Load Previous Experiment']
            self.createExperimentFrame.experimentBox.current(0)
            self.createExperimentFrame.experimentBox.grid(column=3, row=3)
            Label(self.createExperimentFrame, text="Choose Folder: ", font=(12)).grid(column=2, row=4, padx=10, pady=10)
            self.createExperimentFrame.entryValue=Entry(self.createExperimentFrame, textvariable=self.folderName)
            self.createExperimentFrame.entryValue.grid(column=3, row=4)
            Label(self.createExperimentFrame, text="Choose Experiment Set-up: ", font=(12)).grid(column=2, row=5, padx=10, pady=10)
            self.createExperimentFrame.experimentTypeBox = ttk.Combobox(self.createExperimentFrame, textvariable=self.experimentType)
            self.createExperimentFrame.experimentTypeBox['values'] = ['2 Level Fractional Factorial', 'Central Composite Design']
            self.createExperimentFrame.experimentTypeBox.current(0)
            self.createExperimentFrame.experimentTypeBox.grid(column=3, row=5)
            self.createExperimentFrame.nextButton= Button(self.createExperimentFrame, text="Next", command=self.goToInitExperiment)
            self.createExperimentFrame.nextButton.grid(column=6, row=8, padx=5)
            self.createExperimentFrame.cancelButton= Button(self.createExperimentFrame, text="Cancel", command=self.quit)
            self.createExperimentFrame.cancelButton.grid(column=5, row=8, padx=5)
            self.createExperimentFrame.pack()
            
    def goToInitExperiment(self):
        self.createExperimentFrame.pack_forget()
        self.makeCreateExperimentFrame(Shown=False)
        self.makeInitExperimentFrame(Shown=True)
    def linRegressExperiment(self):
        self.title("Fitting data...")
        try:
            experimentOp=ExperimentOperator()
            fName=(self.folderName.get())
            exName=self.experimentName.get()
            fullFileName= (fName + '/' + exName +'-' + self.experimentType.get() + '.csv')
            experimentOp.readExperimentFromCSV(self.experiment, fullFileName)
            i=0
            while(i<len(self.experiment.results)):
                if(i<len(self.experiment.factorWeights)):
                    print("This Weight is already done")
                    i=i+1
                if(i>=len(self.experiment.factorWeights)):
                    experimentOp.linearRegression(i, self.experiment)
                i=i+1
            experimentOp.writeExperimentToCSV(self.experiment, fullFileName)
        except:
            experimentOp=ExperimentOperator()
            fName=(self.folderName.get())
            exName=self.experimentName.get()
            fullFileName= (fName + '/' + exName +'-' + self.experimentType.get() + '.csv')
            i=0
            while(i<len(self.experiment.results)):
                if(i<len(self.experiment.factorWeights)):
                    print("This Weight is already done")
                    i=i+1
                if(i>=len(self.experiment.factorWeights)):
                    experimentOp.linearRegression(i, self.experiment)
                i=i+1
            experimentOp.writeExperimentToCSV(self.experiment, fullFileName)
    def goToCreateExperiment(self):
        #self.initExperimentFrame=self.makeInitExperimentFrame(Shown=False)
        self.initExperimentFrame.pack_forget()
        self.makeCreateExperimentFrame(Shown=True)
    def getExperimentResults(self):
        self.title("Getting Results...")
        experimentOp=ExperimentOperator()
        fName=(self.folderName.get())
        exName=self.experimentName.get()
        fullFileName= (fName + '/' + exName +'-' + self.experimentType.get() + '.csv')
        experimentOp.readExperimentFromCSV(self.experiment, fullFileName)
        self.title("Design of Experiments: Experiment Analysis")
    def graphExperiment(self):
        
        try:
            experimentOp=ExperimentOperator()
            if(self.graphType.get()=="Distribution" ):
                experimentOp.graphExperimentDistribution(self.experiment)
            elif(self.graphType.get()=="Factor Significance"):
                experimentOp.graphExperimentFactorSignificance(self.experiment)
        except:
            self.getExperimentResults()
            experimentOp=ExperimentOperator()
            if(self.graphType.get()=="Distribution" ):
                experimentOp.graphExperimentDistribution(self.experiment)
            elif(self.graphType.get()=="Factor Significance"):
                experimentOp.graphExperimentFactorSignificance(self.experiment)
    def initExperiment(self):
        if(self.experimentType.get()== '2 Level Fractional Factorial'):
            fName=(self.folderName.get())
            exName=self.experimentName.get()
            fullFileName= (fName + '/' + exName +'-' + self.experimentType.get() + '.csv')
            factorList= list((self.listFactors.get()).split(','))
            factorLows=  list([self.factorLows.get()] * int(self.numFactors.get()))
            factorHighs= list([self.factorHighs.get()] * int(self.numFactors.get()))
            generatorList= str(self.fractFactGeneratorDict[self.factorGenerator.get()])
            fixedVariables= list((self.listFixedFactors.get()).split(','))
            experiment=Experiment(factorList=factorList, fixedVariables=fixedVariables, factorHighs=factorHighs, factorLows=factorLows, generatorList=generatorList)
            experimentOp=ExperimentOperator()
            experimentOp.setRunTable(experiment)
            experimentOp.writeExperimentToCSV(experiment, fullFileName )
            self.quit()
        
            
        elif(self.experimentType.get()== 'Central Composite Design'):
            exName=self.experimentName.get()
            fName=(self.folderName.get())
            exName=self.experimentName.get()
            fullFileName= (fName + '/' + exName +'-' + self.experimentType.get() + '.csv')
            factorList= list((self.listFactors.get()).split(','))
            factorLows=  list([self.factorLows.get()] * int(self.numFactors.get()))
            factorHighs= list([self.factorHighs.get()] * int(self.numFactors.get()))
            generatorList= str(self.centralCompositeDesignGeneratorDict[int(self.numFactors.get())])
            experiment=Experiment(factorList=factorList, factorHighs=factorHighs, factorLows=factorLows, generatorList=generatorList)
            experimentOp=ExperimentOperator()
            experimentOp.setRunTable(experiment, Type='CCD')
            experimentOp.writeExperimentToCSV(experiment, fullFileName )
            
    def makeInitExperimentFrame(self, Shown=False):
        self.initExperimentFrame=ttk.Frame()
        if(Shown==True and self.loadExperiment.get()=='Create New Experiment'):
            self.title("Design of Experiments: Initialize Fractional Factorial")
            self.geometry("650x450+350+350")  
            if(self.experimentType.get()=='2 Level Fractional Factorial' and self.loadExperiment.get()=='Create New Experiment'):
                
                Label(self.initExperimentFrame, text="Choose Number of Factors: ", font=(12)).grid(column=2, row=2, padx=10, pady=10)
                self.initExperimentFrame.factorSpin=Spinbox(self.initExperimentFrame, textvariable=self.numFactors, from_ = 5, to = 15)
                self.initExperimentFrame.factorSpin.grid(column=3, row=2)
                Label(self.initExperimentFrame, text="Choose Design: ", font=(12)).grid(column=2, row=4, padx=10, pady=10)
                self.initExperimentFrame.experimentBox = ttk.Combobox(self.initExperimentFrame, textvariable=self.factorGenerator)
                self.initExperimentFrame.experimentBox['values'] = self.fracFactRunList
                self.initExperimentFrame.experimentBox.current(0)
                self.initExperimentFrame.experimentBox.grid(column=3, row=4)
            elif(self.experimentType.get()=='Central Composite Design' and self.loadExperiment.get()=='Create New Experiment'):
                Label(self.initExperimentFrame, text="Choose Number of Factors: ", font=(12)).grid(column=2, row=2, padx=10, pady=10)
                self.initExperimentFrame.factorSpin=Spinbox(self.initExperimentFrame, textvariable=self.numFactors, from_ = 2, to = 15)
                self.initExperimentFrame.factorSpin.grid(column=3, row=2)
            
            Label(self.initExperimentFrame, text="Choose Experiment Name: ", font=(12)).grid(column=2, row=1, padx=10, pady=10)  
            self.initExperimentFrame.entryValue=Entry(self.initExperimentFrame, textvariable=self.experimentName)
            self.initExperimentFrame.entryValue.grid(column=3, row=1)
            Label(self.initExperimentFrame, text="List Variables:(separated by ',')", font=(12)).grid(column=2, row=3, padx=10, pady=10)  
            self.initExperimentFrame.entryValue=Entry(self.initExperimentFrame, textvariable=self.listFactors)
            self.initExperimentFrame.entryValue.grid(column=3, row=3)
            Label(self.initExperimentFrame, text="Choose Factor Low: ", font=(12)).grid(column=2, row=5, padx=10, pady=10)
            self.initExperimentFrame.factorLowSpin=Spinbox(self.initExperimentFrame, textvariable=self.factorLows, from_ = 0, to = 100)
            self.initExperimentFrame.factorLowSpin.grid(column=3, row=5)
            Label(self.initExperimentFrame, text="Choose Factor High: ", font=(12)).grid(column=2, row=6, padx=10, pady=10)
            self.initExperimentFrame.factorHighSpin=Spinbox(self.initExperimentFrame, textvariable=self.factorHighs, from_ = 0, to = 100)
            self.initExperimentFrame.factorHighSpin.grid(column=3, row=6)
            Label(self.initExperimentFrame, text="List Fixed Variables: ", font=(12)).grid(column=2, row=7, padx=10, pady=10)  
            self.initExperimentFrame.entryFixedValue=Entry(self.initExperimentFrame, textvariable=self.listFixedFactors)
            self.initExperimentFrame.entryFixedValue.grid(column=3, row=7)
            
            self.initExperimentFrame.nextButton= Button(self.initExperimentFrame, text="Execute", command = self.initExperiment)
            self.initExperimentFrame.nextButton.grid(column=6, row=9, padx=5)
            self.initExperimentFrame.backButton= Button(self.initExperimentFrame, text="Back", command=self.goToCreateExperiment)
            self.initExperimentFrame.backButton.grid(column=5, row=9, padx=5)
            self.initExperimentFrame.cancelButton= Button(self.initExperimentFrame, text="Cancel", command=self.quit)
            self.initExperimentFrame.cancelButton.grid(column=4, row=9, padx=5)
            self.initExperimentFrame.pack()
        elif(Shown==True and self.loadExperiment.get()== 'Load Previous Experiment'):
            self.title("Design of Experiments: Experiment Analysis")
            self.geometry("650x450+350+350")
            Label(self.initExperimentFrame, text="Experiment Name: ", font=(12)).grid(column=2, row=2, padx=10, pady=10)  
            self.initExperimentFrame.entryValue=Entry(self.initExperimentFrame, textvariable=self.experimentName)
            self.initExperimentFrame.entryValue.grid(column=3, row=2)
            self.initExperimentFrame.resultsButton= Button(self.initExperimentFrame, text="Get Results", command = self.getExperimentResults)
            self.initExperimentFrame.resultsButton.grid(column=5, row=2, padx=5, pady=5)
            
            Label(self.initExperimentFrame, text="Choose Graph Design: ", font=(12)).grid(column=2, row=3, padx=10, pady=10)
            self.initExperimentFrame.graphBox = ttk.Combobox(self.initExperimentFrame, textvariable=self.graphType)
            self.initExperimentFrame.graphBox['values'] = self.graphList
            self.initExperimentFrame.graphBox.current(0)
            self.initExperimentFrame.graphBox.grid(column=3, row=3, padx=5, pady=5)
            self.initExperimentFrame.graphButton= Button(self.initExperimentFrame, text="Graph", command = self.graphExperiment)
            self.initExperimentFrame.graphButton.grid(column=5, row=3, padx=5, pady=5)
            
            
            Label(self.initExperimentFrame, text="Choose Type of Fit: ", font=(12)).grid(column=2, row=4, padx=10, pady=10)
            self.initExperimentFrame.regressfitBox = ttk.Combobox(self.initExperimentFrame, textvariable=self.fitType)
            self.initExperimentFrame.regressfitBox['values'] = self.fitList
            self.initExperimentFrame.regressfitBox.current(0)
            self.initExperimentFrame.regressfitBox.grid(column=3, row=4, padx=5, pady=5)
            self.initExperimentFrame.regressfitButton= Button(self.initExperimentFrame, text="Fit Data", command = self.linRegressExperiment)
            self.initExperimentFrame.regressfitButton.grid(column=5, row=4, padx=5, pady=5)
            
            self.initExperimentFrame.finishButton= Button(self.initExperimentFrame, text="Finish", command = self.initExperiment)
            self.initExperimentFrame.finishButton.grid(column=6, row=8, padx=5)
            self.initExperimentFrame.backButton= Button(self.initExperimentFrame, text="Back", command=self.goToCreateExperiment)
            self.initExperimentFrame.backButton.grid(column=5, row=8, padx=5)
            self.initExperimentFrame.cancelButton= Button(self.initExperimentFrame, text="Cancel", command=self.quit)
            self.initExperimentFrame.cancelButton.grid(column=4, row=8, padx=5)
            self.initExperimentFrame.pack()
            
            
myGui= MainDialog()
myGui.mainloop()
