import tkinter as tk
from tkinter import ttk
from Database.database import *

class Contabilitate(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,background="bisque")
        tk.Label(self,text="Contabilitate",font = ("Verdana",18),background="bisque").pack(pady=10,padx=0)
        self.closeButton = tk.Button(self,text= "Mergi inapoi",font=("Verdana",13),command = lambda: controller.show_frame("StartPage"))
        self.closeButton.pack(pady = 10,padx = 5)
        self.tempList = []
        self.cols = None
        self.listBox = None

        self.farmacii = None
        self.nr_med_vandute = {}
        self.status_vanzari = {}
        self.status_brut = {}
        self.valoare_vanzari = [0,0,0]
        self.valoare_brut = [0,0,0]
        self.profit = [0,0,0]



    def Show(self,cont):
        if self.listBox != None:
            self.listBox.destroy()
        self.GetValues()
        self.listBox = ttk.Treeview(self,columns = self.cols,show = 'headings')
        for i,row in enumerate(self.tempList,start=1):
            values = [i]
            for element in row:
                values.append(element)
            self.listBox.insert("","end",values=values)

        for col in self.cols:
            self.listBox.heading(col,text=col)
        self.listBox.pack(pady = 40,padx = 10)
        self.closeButton.pack_forget()
        self.closeButton.pack(pady=10,padx=40)

    def GetValues(self):
        self.cols = ['INDEX','FARMACIA','MEDICAMENTE VANDUTE','VALOARE VANZARE','VALOARE CUMPARARE','PROFIT','CHELTUIELI']
        self.tempList = []
        self.nr_med_vandute = {}
        self.status_vanzari = {}
        self.status_brut = {}
        self.valoare_vanzari = [0,0,0]
        self.valoare_brut = [0,0,0]
        self.profit = [0,0,0]

        self.farmacii = DataBaseOperations.ExtractColumnsWithCondition(database.cursor_,"FARMACII",
                                                                       ['ID_FARMACIE'],0)

        self.farmacii = [(farmacia[0],'Farma -- {}'.format(farmacia[0])) for farmacia in self.farmacii]


        for farmacie in self.farmacii:
            nr_med = DataBaseOperations.ExtractSoldQuantityPerPharma(database.cursor_,farmacie[0])
            self.nr_med_vandute[farmacie[0]] = nr_med[0][0]

            situatie_vanzare = DataBaseOperations.ExtractSalesStatus(database.cursor_,farmacie[0]) # 0 ANGAJAT 1 : CANTITATE 2 ID 3 valoarea
            self.status_vanzari[farmacie[0]] = situatie_vanzare

            situatie_vanzare = DataBaseOperations.ExtractGrossPrice(database.cursor_,farmacie[0])
            self.status_brut[farmacie[0]] = situatie_vanzare


        for idx,farmacie in enumerate(self.farmacii):
            for element in self.status_vanzari[farmacie[0]]:
                self.valoare_vanzari[idx] += element[3]


            for element in self.status_brut[farmacie[0]]:
                self.valoare_brut[idx] += element[3]

            self.profit[idx] = self.valoare_vanzari[idx] - self.valoare_brut[idx]


        for idx,farmacie in enumerate(self.farmacii):
            temp = [farmacie[0],
                    self.nr_med_vandute[farmacie[0]],
                    round(self.valoare_vanzari[idx],2),
                    round(self.valoare_brut[idx],2),
                    round(self.profit[idx],2),
                    round(costs[int(farmacie[0]) % 2000],2)]
            self.tempList.append(temp)