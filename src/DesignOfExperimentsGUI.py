'''
Created on Jul 10, 2014

@author: vpsmith
'''
from tkinter import *
from tkinter import ttk




class MainDialog:
    def __init__(self, parent):
        self.parent = parent
        self.value_of_combo = 'Create New Experiment'
        Label(self.parent, text="Choose Configuration: ", font=(12)).grid(column=2, row=3, padx=10, pady=10)
        self.combo(('Create New Experiment', 'Load Previous Experiment'), 3, 3)
        Label(self.parent, text="Choose File: ", font=(12)).grid(column=2, row=4, padx=10, pady=10)
        self.entryValue=Entry(self.parent)
        #self.directory = filedialog
        #self.directory.askdirectory(initialdir='.')
        self.entryValue.grid(column=3, row=4)
        Label(self.parent, text="Choose Experiment Set-up: ", font=(12)).grid(column=2, row=5, padx=10, pady=10)
        self.combo(('2 Level Fractional Factorial', 'Central Composite Design'), 5, 3)
        
        self.nextButton= Button(self.parent, text="Next")
        self.nextButton.grid(column=4, row=8, padx=5)
        self.nextButton= Button(self.parent, text="Cancel", command=self.parent.quit)
        self.nextButton.grid(column=3, row=8, padx=5)
    
    def newselection(self, event):
        self.value_of_combo = self.box.get()
        print(self.value_of_combo)
        print(self.entryValue.get())
#
    def combo(self, values, row, col):
        self.box_value = StringVar()
        self.box = ttk.Combobox(self.parent, textvariable=self.box_value)
        self.box.bind("<<ComboboxSelected>>", self.newselection)
        self.box['values'] = values
        self.box.current(0)
        self.box.grid(column=col, row=row)
    #def continueMain(self):
      #  self.parent.

    
class CreateExperiment(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Create Your Own Experiment") 
        
        self.pack(fill=BOTH, expand=1)

        runs = ['Two Level Fractional Factorial', '' ]

        lb = Listbox(self)
        for i in runs:
            lb.insert(END, i)
            
        lb.bind("<<ListboxSelect>>", self.onSelect)    
            
        lb.place(x=20, y=20)

        self.var = StringVar()
        self.label = Label(self, text=0, textvariable=self.var)        
        self.label.place(x=20, y=210)

    def onSelect(self, val):
      
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)   

        self.var.set(value)
         

def main():
  
    root = Tk()
    ex = MainDialog(root)
    root.geometry("550x200+350+350")
    root.mainloop()  


if __name__ == '__main__':
    main()  



