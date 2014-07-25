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
        self.listResults= StringVar()
        self.factorLows=StringVar()
        self.factorHighs=StringVar()
        self.numFactors=StringVar()
        self.factorGenerator=StringVar()
        self.listSignificantFactors=[]
        self.listFactorWeights=[]
        self.fracFactRunList=["5 Factor Design(16 Runs and Resolution V)", "9 Factor Design (32 Runs and Resolution IV)"]
        self.fractFactGeneratorDict = {"5 Factor Design(16 Runs and Resolution V)":'a b c d e', "9 Factor Design (32 Runs and Resolution IV)": 'a b c d e bcde acde abde abce'}
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
    
    def goToCreateExperiment(self):
        #self.initExperimentFrame=self.makeInitExperimentFrame(Shown=False)
        self.initExperimentFrame.pack_forget()
        self.makeCreateExperimentFrame(Shown=True)
    
    def initExperiment(self):
        if(self.experimentType.get()== '2 Level Fractional Factorial'):
            factorList= list((self.listFactors.get()).split(','))
            factorLows=  list([self.factorLows.get()] * int(self.numFactors.get()))
            factorHighs= list([self.factorHighs.get()] * int(self.numFactors.get()))
            generatorList= str(self.fractFactGeneratorDict[self.factorGenerator.get()])
            experiment=Experiment(factorList=factorList, factorHighs=factorHighs, factorLows=factorLows, generatorList=generatorList)
            
            
            
            
        elif(self.experimentType.get()== 'Central Composite Design'):
            fName=self.experimentName.get()
            
    def makeInitExperimentFrame(self, Shown=False):
        if(Shown==True and self.loadExperiment.get()=='Create New Experiment'):
            self.title("Design of Experiments: Initialize Fractional Factorial")
            self.geometry("650x450+350+350")  
            if(self.experimentType.get()=='2 Level Fractional Factorial'):
                
                Label(self.initExperimentFrame, text="Choose Number of Factors: ", font=(12)).grid(column=2, row=2, padx=10, pady=10)
                self.initExperimentFrame.factorSpin=Spinbox(self.initExperimentFrame, textvariable=self.numFactors, from_ = 5, to = 15)
                self.initExperimentFrame.factorSpin.grid(column=3, row=2)
                Label(self.initExperimentFrame, text="Choose Design: ", font=(12)).grid(column=2, row=4, padx=10, pady=10)
                self.initExperimentFrame.experimentBox = ttk.Combobox(self.initExperimentFrame, textvariable=self.factorGenerator)
                self.initExperimentFrame.experimentBox['values'] = self.fracFactRunList
                self.initExperimentFrame.experimentBox.current(0)
                self.initExperimentFrame.experimentBox.grid(column=3, row=4)
            
            Label(self.initExperimentFrame, text="Choose Experiment Name: ", font=(12)).grid(column=2, row=1, padx=10, pady=10)  
            self.initExperimentFrame.entryValue=Entry(self.initExperimentFrame, textvariable=self.experimentName)
            self.initExperimentFrame.entryValue.grid(column=3, row=1)
            Label(self.initExperimentFrame, text="List Variables: ", font=(12)).grid(column=2, row=3, padx=10, pady=10)  
            self.initExperimentFrame.entryValue=Entry(self.initExperimentFrame, textvariable=self.listFactors)
            self.initExperimentFrame.entryValue.grid(column=3, row=3)
            Label(self.initExperimentFrame, text="Choose Factor Low: ", font=(12)).grid(column=2, row=5, padx=10, pady=10)
            self.initExperimentFrame.factorLowSpin=Spinbox(self.initExperimentFrame, textvariable=self.factorLows, from_ = 0, to = 100)
            self.initExperimentFrame.factorLowSpin.grid(column=3, row=5)
            Label(self.initExperimentFrame, text="Choose Factor High: ", font=(12)).grid(column=2, row=6, padx=10, pady=10)
            self.initExperimentFrame.factorHighSpin=Spinbox(self.initExperimentFrame, textvariable=self.factorHighs, from_ = 0, to = 100)
            self.initExperimentFrame.factorHighSpin.grid(column=3, row=6)
            
            self.initExperimentFrame.nextButton= Button(self.initExperimentFrame, text="Execute", command = self.initExperiment)
            self.initExperimentFrame.nextButton.grid(column=6, row=8, padx=5)
            self.initExperimentFrame.backButton= Button(self.initExperimentFrame, text="Back", command=self.goToCreateExperiment)
            self.initExperimentFrame.backButton.grid(column=5, row=8, padx=5)
            self.initExperimentFrame.cancelButton= Button(self.initExperimentFrame, text="Cancel", command=self.quit)
            self.initExperimentFrame.cancelButton.grid(column=4, row=8, padx=5)
            self.initExperimentFrame.pack()
        if(Shown==True and self.loadExperiment.get()== 'Load Previous Experiment'):
            self.title("Design of Experiments: Experiment Analysis")
            self.geometry("650x450+350+350")
            
            
myGui= MainDialog()
myGui.mainloop()
