import tkinter as tk
from tkinter import ttk
from Database.database import *


class ActualizareStoc(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,background="bisque")
        tk.Label(self,text="Actualizare Stoc",font=("Verdana",20),background="bisque").pack(pady=5,padx=0)


        self.farmacie = {
            'mapa'        : None,
            'selectie_id' : None,
            'combobox'    : None
        }

        self.distribuitor = {
            'selectie_id' : None,
            'text'         : tk.StringVar(),
            'label'       : None
        }

        self.medicament = {
            'selectie_id' : None,
            'mapa' : None,
            'combobox' : None

        }

        self.status_label = {
            'var'   : tk.StringVar(),
            'label' : None
        }
        self.distribuitor['text'].set('-')
        self.cantitate_selectie = tk.StringVar()
        self.cantitate_selectie.set('-')
        self.pret_selectie = tk.StringVar()
        self.pret_selectie.set('-')


        self.CreateComboboxes()
        tk.Button(self,text="Mergi inapoi",command = lambda: controller.show_frame('StartPage')).pack(pady = 10,padx=0)

    def CreateComboboxes(self):
        tk.Label(self,text="Selectati farmacia",font=("Verdana",14),background="bisque").pack(pady=20,padx=0)
        self.farmacie['mapa'] = DataBaseOperations.ExtractColumnsWithCondition(database.cursor_,"FARMACII",["ID_FARMACIE"],0)
        self.farmacie['mapa'] = ["FARMACIA " + str(element) for element in range(1,4)]
        self.farmacie['combobox'] = ttk.Combobox(self,values=self.farmacie['mapa'],state='readonly')
        self.farmacie['combobox'].bind('<<ComboboxSelected>>',self.Farma_Selected)
        self.farmacie['combobox'].pack(pady=5,padx=0)
        self.farmacie['combobox'].current(0)


        tk.Label(self,text = "Distribuitor",font=("Verdana",14),background="bisque").pack(pady=25,padx=0)
        self.distribuitor['label'] =  tk.Label(self,textvariable = self.distribuitor['text'],font=("Verdana",14),background="bisque")
        self.distribuitor['label'].pack(pady = 5,padx = 0)

        tk.Label(self,text = "Alegeti medicamentul",font=("Verdana",13),background="bisque").pack(pady=25,padx=0)
        self.medicament['combobox'] = ttk.Combobox(self,values=[],state='readonly',width = 30)
        self.medicament['combobox'].bind('<<ComboboxSelected>>',self.Medicament_Selected)
        self.medicament['combobox'].pack(pady = 5,padx = 0)

        tk.Label(self,text="Stoc disponibil",font=("Verdana",13),background="bisque").pack(pady=15,padx=0)
        tk.Label(self,textvariable = self.cantitate_selectie,font=("Verdana",13),background="bisque").pack(pady=5,padx=0)

        tk.Label(self,text="Pret per unitate",font=("Verdana",13),background="bisque").pack(pady=10,padx=0)
        tk.Label(self,textvariable = self.pret_selectie,font=("Verdana",13),background="bisque").pack(pady=5,padx=0)

        tk.Label(self,text="Introduceti cantitate dorita",font=("Verdana",13),background="bisque").pack(pady=10,padx=0)
        self.cantitate = tk.StringVar()
        self.cantitate_dorita = tk.Entry(self,width=20,textvariable=self.cantitate)
        self.old_value = ''
        self.cantitate.trace('w',self.Cantitate_Digit_Check)
        self.cantitate_dorita.pack(pady = 5,padx = 0)

        self.status_label['var'].set('-')
        self.status_label['label'] = tk.Label(self,textvariable = self.status_label['var'],font = ("Verdana",13),background="bisque")
        self.status_label['label'].pack(pady=5,padx=0)

        tk.Button(self,text="Cumpara",font=("Verdana",13),command = lambda: self.Achizitie()).pack(pady=5,padx=0)

    def Farma_Selected(self,event):
        text = self.farmacie['combobox'].get()
        self.farmacie['selectie_id'] = str(2000 + int(text[text.find(" ")+1:]) - 1)
        self.distribuitor['selectie_id'] = DataBaseOperations.ExtractColumnsWithCondition(database.cursor_,
                                                                                          "FARMACII",["ID_DISTRIBUITOR"],
                                                                                          "ID_FARMACIE = {}".format(self.farmacie['selectie_id']))[0][0]

        nume_distribuitor = DataBaseOperations.ExtractColumnsWithCondition(database.cursor_,
                                                                           "DISTRIBUITORI",["NUME"],
                                                                           "ID_DISTRIBUITOR = {}".format(self.distribuitor['selectie_id']))[0][0]

        self.distribuitor['text'].set(nume_distribuitor)

        self.medicament['mapa'] = DataBaseOperations.ExtractColumnsWithCondition(database.cursor_,
                                                                                 "DEPOZITE",["ID_MEDICAMENT","STOC","PRET"],
                                                                                 "ID_DISTRIBUITOR = {}".format(self.distribuitor['selectie_id']))


        self.nume_medicamente = DataBaseOperations.GetDrugNameFromDeposits(database.cursor_,self.distribuitor['selectie_id'])
        self.medicament['combobox']['values'] = [medicament[1] for medicament in self.nume_medicamente]
        self.medicament['combobox'].current(0)


    def Medicament_Selected(self,event):
        combo_result = self.medicament['combobox'].get()
        for field in self.nume_medicamente:
            if field[1] == combo_result:
                self.medicament['selectie_id'] = str(field[0])
                break

        for element in self.medicament['mapa']:
            if int(element[0]) == int(self.medicament['selectie_id']):
                self.cantitate_selectie.set(element[1])
                self.pret_selectie.set(element[2])
                break


    def Cantitate_Digit_Check(self,*args):
        if self.cantitate.get().isdigit():
            self.old_value = self.cantitate.get()
        else:
            self.cantitate.set(self.old_value)

    def Achizitie(self):
        global costs
        cantitate = self.cantitate_dorita.get()
        if int(cantitate) < int(self.cantitate_selectie.get()):
            pret = round(int(cantitate) * float(self.pret_selectie.get()),2)
            costs[int(self.farmacie['selectie_id']) % 2000] += pret
            self.status_label['var'].set('Tranzactie realizata cu succes. Aveti de achitat suma de {}'.format(pret))
            self.UpdateStoc(cantitate)
            self.UpdateDepozite(cantitate)
        else:
            self.status_label['var'].set('Cantitatea dorita este indisponibila')

    def UpdateStoc(self,cantitate):
        DataBaseOperations.AlterInventory(database.connection,-int(cantitate),
                                          self.farmacie['selectie_id'],
                                          self.medicament['selectie_id'])
    def UpdateDepozite(self,cantitate):
        DataBaseOperations.AlterDeposits(database.connection,int(cantitate),
                                         self.medicament['selectie_id'],
                                         self.distribuitor['selectie_id'])
        self.cantitate_selectie.set(int(self.cantitate_selectie.get()) - int(cantitate))
