import tkinter as tk
from tkinter import ttk
from Database.database import *


class DisplayTables(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent,background="bisque")
        controller.resizable(False,False)
        tk.Label(self, text="PHARMAPLUS", font=("Verdana", 20),background="bisque").pack(pady=20,padx=20)
        tk.Button(self, text="AFISARE TABELA FARMACII",command=lambda: controller.show_frame('DTL_FARMACII')).pack(pady = 20,padx = 20)
        tk.Button(self,text = "AFISARE TABELA LOCATII",command = lambda:controller.show_frame('DTL_LOCATII')).pack(pady=10,padx = 20)
        tk.Button(self, text="AFISARE TABELA ANGAJATI",command=lambda: controller.show_frame('DTL_ANGAJATI')).pack(pady = 20,padx = 20)
        tk.Button(self,text = "AFISARE TABELA DEPOZITE",command = lambda:controller.show_frame('DTL_DEPOZITE')).pack(pady = 10,padx = 20)
        tk.Button(self, text="AFISARE TABELA DISTRIBUITORI",command=lambda: controller.show_frame('DTL_DISTRIBUITORI')).pack(pady = 20,padx = 20)
        tk.Button(self,text = "AFISARE TABELA MEDICAMENTE",command = lambda:controller.show_frame('DTL_MEDICAMENTE')).pack(pady=10,padx = 20)
        tk.Button(self, text="AFISARE TABELA STOCURI",command=lambda:controller.show_frame('DTL_STOCURI')).pack(pady = 20,padx = 20)
        tk.Button(self,text = "AFISARE TABELA VANZARI",command = lambda:controller.show_frame('DTL_VANZARI')).pack(pady=10,padx = 20)
        tk.Button(self, text="Mergi inapoi", width=15, command=lambda: controller.show_frame('StartPage')).pack(pady = 10,padx = 40)



class DisplayTableLayout(tk.Frame):
    def __init__(self, parent, controller,tablename):
        tk.Frame.__init__(self, parent,background="bisque")
        self.tablename = tablename
        self.closeButton = tk.Button(self, text="Mergi inapoi", width=15, command=lambda: controller.show_frame('DisplayTables'))
        self.closeButton.pack(pady = 10,padx = 40)
        self.cols = ['INDEX']
        self.drug_id_label = None
        self.tempList = None
        self.listBox = None
        self.druglabel = None
        self.drug_id_label = None
        self.drug_search = None
        self.drugbutton = None

    def Show(self,cont):
        print(cont)
        if self.listBox != None:
            self.listBox.destroy()
            self.tempList = DataBaseOperations.GetAllFromTable(database.cursor_,self.tablename)
        else:
            tk.Label(self, text=self.tablename, font=("Arial",30),background="bisque").pack(pady = 10,padx = 40)
            self.cols.extend(DataBaseOperations.GetTableDescription(database.cursor_,self.tablename))
            self.tempList = DataBaseOperations.GetAllFromTable(database.cursor_,self.tablename)
        self.listBox = ttk.Treeview(self, columns= self.cols, show='headings')
        for i, row in enumerate(self.tempList, start=1):
            values = [i]
            for element in row:
                values.append(element)
            self.listBox.insert("", "end", values=values)

        for col in self.cols:
            self.listBox.heading(col, text = col)
        self.listBox.pack(pady = 40,padx = 10)
        fields = ['STOCURI','VANZARI','DEPOZITE','MEDICAMENTE']
        conditions = []
        condition = False
        for field in fields:
            conditions.append(cont.find(field) > 0)
        for cnd in conditions:
            if cnd:
                condition = True
                break
        if condition:
            if self.druglabel != None:
                self.druglabel.destroy()
            if self.drug_id_label != None:
                self.drug_id_label.destroy()
            if self.drug_search != None:
                self.drug_search.destroy()
            if self.drugbutton != None:
                self.drugbutton.destroy()
            self.druglabel = tk.Label(self,text = 'Medicamentul cautat',font=("Verdana", 15),background="bisque")
            self.druglabel.pack(padx=10,pady=10)
            self.drug_search = tk.Entry(self,width=20,text='-')
            self.drug_search.pack(pady = 10,padx = 10)
            self.drug_id_label = tk.Label(self,text = "" ,font=("Verdana", 15),background="bisque")
            self.drugbutton = tk.Button(self,text = 'Obtine ID',width=15,command = lambda : self.GetDrugId(self.drug_search))
            self.drugbutton.pack(pady = 10,padx = 10)
        self.closeButton.pack_forget()
        self.closeButton.pack(pady = 10,padx = 40)


    def GetDrugId(self,field):
        drugName = field.get()
        id = DataBaseOperations.ExtractColumnsWithCondition(database.cursor_,'MEDICAMENTE',{'ID_MEDICAMENT'},'NUME = \'{}\''.format(drugName.lower().capitalize()))
        self.drug_id_label.pack_forget()
        self.closeButton.pack_forget()

        if not id:
            self.drug_id_label["text"] = "Nu exista medicamentul cautat"
        else:
            self.drug_id_label["text"] = "ID : {}".format(id[0][0])
        self.drug_id_label.pack(pady = 10,padx = 10)
        self.closeButton.pack(pady = 10,padx = 40)