import tkinter as tk
from tkinter import ttk
from Database.database import *

class Transaction(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent,background="bisque")
        tk.Label(self,text = "Tranzactie",font=("Verdana", 20),background="bisque").pack(pady = 10,padx = 10)
        self.farmacie = {
            'mapa'        : None,
            'combobox'    : None,
            'selectie_id' : None
        }

        self.angajat = {
            'mapa'         : None,
            'combobox'     : None,
            'selectie_id'  : None,
            'selectie_job' : None
        }

        self.medicament = {
            'mapa'     : None,
            'combobox' : None,
            'selectie' : None
        }


        self.CreateComboboxes()
        self.stoc = None


        tk.Button(self,text = "Mergi inapoi",font=("Verdana",14),command = lambda:controller.show_frame("StartPage")).pack(pady = 15,padx = 0)


    def CreateComboboxes(self):
        tk.Label(self,text = "Alegeti farmacia",font=("Verdana",15),background="bisque").pack(pady = 15,padx = 0)
        self.farmacie['mapa'] = DataBaseOperations.ExtractColumnsWithCondition(database.cursor_,"FARMACII",["ID_FARMACIE"],0)
        self.farmacie['mapa'] = ["FARMACIA " + str(element) for element in range(1,4)]
        self.farmacie['combobox'] = ttk.Combobox(self,values = self.farmacie['mapa'],state='readonly')
        self.farmacie['combobox'].bind('<<ComboboxSelected>>',self.Farma_Selected)
        self.farmacie['combobox'].pack(pady=5,padx=0)
        self.farmacie['combobox'].current(0)


        tk.Label(self,text = "Alegeti farmacistul",font=("Verdana",15),background="bisque").pack(pady = 15,padx = 0)
        self.angajat['combobox'] = ttk.Combobox(self,values=[],state='readonly',width = 30)
        self.angajat['combobox'].bind('<<ComboboxSelected>>',self.Farmacist_Selected)
        self.angajat['combobox'].pack(pady = 5,padx = 0)


        tk.Label(self,text = "Alegeti medicamentul",font=("Verdana",15),background="bisque").pack(pady = 15,padx = 0,)
        self.medicament['combobox'] = ttk.Combobox(self,values=[],state='readonly',width = 30)
        self.medicament['combobox'].bind('<<ComboboxSelected>>',self.Medicament_Selected)
        self.medicament['combobox'].pack(pady = 5,padx = 0)


        tk.Label(self,text= "Stoc",font=("Verdana",15),background="bisque").pack(pady = 5,padx = 0)
        self.stoc_var = tk.StringVar(self," -")
        tk.Label(self,textvariable=self.stoc_var,font=("Verdana",13),background="bisque").pack(pady = 5,padx = 0)


        tk.Label(self,text= "Pret",font=("Verdana",15),background="bisque").pack(pady = 5,padx = 0)
        self.pret_var = tk.StringVar(self," -")
        tk.Label(self,textvariable=self.pret_var,font=("Verdana",13),background="bisque").pack(pady = 5,padx =0)


        self.cantitate = tk.StringVar()
        tk.Label(self,text="Cantitatea dorita",font=("Verdana",15),background="bisque").pack(pady = 5,padx = 0)
        self.cantitate_dorita = tk.Entry(self,width=20,textvariable=self.cantitate)
        self.old_value = ''
        self.cantitate.trace('w',self.Cantitate_Digit_Check)
        self.cantitate_dorita.pack(pady = 5,padx = 0)


        tk.Button(self,text="Cumpara",font=("Verdana",15),command = self.Tranzactie).pack(pady = 15,padx = 0)
        self.status_tranzactie_var = tk.StringVar(self," -")
        tk.Label(self,textvariable = self.status_tranzactie_var,font=("Verdana",15),background="bisque").pack(pady=5,padx=0)



    def Farma_Selected(self,event):
        text = self.farmacie['combobox'].get()
        self.farmacie['selectie_id'] = str(2000 + int(text[text.find(" ")+1:]) - 1)
        self.angajat['mapa'] = DataBaseOperations.ExtractEmployeesfromPharma(database.cursor_,str(self.farmacie['selectie_id']))
        self.angajat['combobox']['values'] = ["" + angajat[0] + " - " + angajat[1] for angajat in self.angajat['mapa']]
        self.angajat['combobox'].current(0)


    def Farmacist_Selected(self,event):
        text = self.angajat['combobox'].get()
        for label in self.angajat['mapa']:
            if label[0] == text[:text.find(" -")]:
                self.angajat['selectie_id'] = label[2]
                self.angajat['selectie_job'] = label[1]
                break

        self.medicament['mapa'] = DataBaseOperations.ExtractDrugsForSpecificEmployee(database.cursor_,self.angajat['selectie_job'])
        self.medicament['combobox']['values'] = [medicament[1] for medicament in self.medicament['mapa']]
        self.medicament['combobox'].current(0)


    def Medicament_Selected(self,event):
        text = self.medicament['combobox'].get()
        for label in self.medicament['mapa']:
            if label[1] == text:
                self.medicament['selectie'] = label[0]
                break
        print(self.medicament['selectie'])
        self.stoc = DataBaseOperations.ExtractDrugsInventory(database.cursor_,self.farmacie['selectie_id'],self.medicament['selectie'])
        self.stoc = [self.stoc[0][0],self.stoc[0][1]]
        self.stoc_var.set(str(self.stoc[0]))
        self.pret_var.set(str(self.stoc[1]))


    def Cantitate_Digit_Check(self,*args):
        if self.cantitate.get().isdigit():
            self.old_value = self.cantitate.get()
        else:
            self.cantitate.set(self.old_value)


    def Tranzactie(self):
        if int(self.cantitate.get()) < int(self.stoc[0]):
            nume_medicament = DataBaseOperations.ExtractColumnsWithCondition(database.cursor_,
                                                                             "MEDICAMENTE",["NUME"],
                                                                             "ID_MEDICAMENT = {}".format(self.medicament['selectie']))[0][0]
            self.status_tranzactie_var.set("Ati cumparat {} cutii de {} pentru {} lei.".format(self.cantitate.get(),
                                                                                               nume_medicament,
                                                                                               round(self.stoc[1] * float(self.cantitate.get()),2)))
            self.stoc = self.UpdateStoc(int(self.cantitate.get()))
            self.stoc_var.set(self.stoc[0])
            self.UpdateTabelaVanzari(int(self.cantitate.get()))
        else:
            self.status_tranzactie_var.set("Stoc insuficient de medicamente")
            stocuri_medicament_x = []
            farmacii = DataBaseOperations.ExtractColumnsWithCondition(database.cursor_,"FARMACII",["ID_FARMACIE"],0)
            for farma in farmacii:
                if farma[0] != self.farmacie['selectie_id']:
                    stoc_aux = DataBaseOperations.ExtractDrugsInventory(database.cursor_,
                                                                        farma[0],
                                                                        self.medicament['selectie'])[0][0]
                    stocuri_medicament_x.append([farma[0],stoc_aux])
            found = 0
            for stoc in stocuri_medicament_x:
                if stoc[1]  > int(self.cantitate.get()):
                    found = 1
                    self.status_tranzactie_var.set("Stoc insuficient de medicamente. Puteti incerca la farmacia {}.".format(stoc[0]))
                    break
            if found == 0:
                self.status_tranzactie_var.set("Stoc insuficient de medicamente. Nu gasiti la nicio farmacie cantitatea dorita.")


    def UpdateStoc(self,cantitate):
        DataBaseOperations.AlterInventory(database.connection,
                                          cantitate,
                                          self.farmacie['selectie_id'],
                                          self.medicament['selectie'])


        self.stoc = DataBaseOperations.ExtractDrugsInventory(database.cursor_,
                                                             self.farmacie['selectie_id'],
                                                             self.medicament['selectie'])
        return [self.stoc[0][0],self.stoc[0][1]]


    def UpdateTabelaVanzari(self,cantitate):
        result = DataBaseOperations.InsertCommand(database.connection,"INSERT INTO VANZARI VALUES({},{},{})".format(self.angajat['selectie_id'],
                                                                                                                    self.medicament['selectie'],
                                                                                                                    cantitate))
        print("***")
        print(result[1])
        print("***")
        if result[0] == False:
            DataBaseOperations.AlterSales(database.connection,
                                          cantitate,
                                          self.angajat['selectie_id'],
                                          self.medicament['selectie'])