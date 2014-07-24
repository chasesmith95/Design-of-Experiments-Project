'''
Created on Jul 10, 2014

@author: vpsmith
'''
from tkinter import *
from tkinter import ttk

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
        self.numFactors=StringVar()
        self.factorGenerator=StringVar()
        self.listSignificantFactors=[]
        self.listFactorWeights=[]
        self.fracFactRunList=["5 Factor Design(16 Runs and Resolution V)", "9 Factor Design (32 Runs and Resolution IV)"]
        self.createExperimentFrame= ttk.Frame(self)
        self.initExperimentFrame= ttk.Frame(self)
        self.makeCreateExperimentFrame(Shown=True)
        
       

    def makeCreateExperimentFrame(self, Shown=False):
        if(Shown==True):
            self.title("Design of Experiments: Create Experiment")
            self.geometry("550x200+350+350")
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
            self.createExperimentFrame.nextButton.grid(column=4, row=8, padx=5)
            self.createExperimentFrame.cancelButton= Button(self.createExperimentFrame, text="Cancel", command=self.quit)
            self.createExperimentFrame.cancelButton.grid(column=3, row=8, padx=5)
            self.createExperimentFrame.pack()
            
    def goToInitExperiment(self):
        self.createExperimentFrame.pack_forget()
        self.initExperimentFrame=self.makeInitExperimentFrame(Shown=True)
        
    def makeInitExperimentFrame(self, Shown=False):
        if(Shown==True):
            self.title("Design of Experiments: Initialize Fractional Factorial")
            self.geometry("500x500+350+350")  
            if(self.experimentType.get()=='2 Level Fractional Factorial'):
                
                Label(self.initExperimentFrame, text="Choose Number of Factors: ", font=(12)).grid(column=2, row=3, padx=10, pady=10)
                self.initExperimentFrame.factorSpin=Spinbox(self.initExperimentFrame, textvariable=self.numFactors, from_ = 5, to = 15)
                self.initExperimentFrame.factorSpin.grid(column=3, row=3)
                Label(self.initExperimentFrame, text="Choose Design: ", font=(12)).grid(column=2, row=4, padx=10, pady=10)
                self.initExperimentFrame.experimentBox = ttk.Combobox(self.initExperimentFrame, textvariable=self.factorGenerator)
                self.initExperimentFrame.experimentBox['values'] = self.fracFactRunList
                self.initExperimentFrame.experimentBox.current(0)
                self.initExperimentFrame.experimentBox.grid(column=3, row=4)
            
            Label(self.initExperimentFrame, text="Choose Experiment Name: ", font=(12)).grid(column=2, row=1, padx=10, pady=10)  
            self.initExperimentFrame.entryValue=Entry(self.initExperimentFrame, textvariable=self.experimentName)
            self.initExperimentFrame.entryValue.grid(column=3, row=1)
            Label(self.initExperimentFrame, text="List Variables: ", font=(12)).grid(column=2, row=2, padx=10, pady=10)  
            self.initExperimentFrame.entryValue=Entry(self.initExperimentFrame, textvariable=self.listFactors)
            self.initExperimentFrame.entryValue.grid(column=3, row=2)
            self.initExperimentFrame.pack()
            
myGui= MainDialog()
myGui.mainloop()
