import tkinter as tk
from tkinter import ttk
import time
from database import *


costs = [0,0,0]
database = DataBase()


class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(fill=None, expand=False)

        self.frames = {}
        for F in (DBConnect,StartPage,DisplayTables,InitDataBase,Transaction,ActualizareStoc,Contabilitate):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame

        self.frames['DTL_ANGAJATI'] = DisplayTableLayout(self.container,self,'ANGAJATI')
        self.frames['DTL_DEPOZITE'] = DisplayTableLayout(self.container,self,'DEPOZITE')
        self.frames['DTL_DISTRIBUITORI'] = DisplayTableLayout(self.container,self,'DISTRIBUITORI')
        self.frames['DTL_FARMACII'] = DisplayTableLayout(self.container,self,'FARMACII')
        self.frames['DTL_LOCATII'] = DisplayTableLayout(self.container,self,'LOCATII')
        self.frames['DTL_MEDICAMENTE'] = DisplayTableLayout(self.container,self,'MEDICAMENTE')
        self.frames['DTL_STOCURI'] = DisplayTableLayout(self.container,self,'STOCURI')
        self.frames['DTL_VANZARI'] = DisplayTableLayout(self.container,self,'VANZARI')

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame('DBConnect')

    def show_frame(self, cont):
        frame = self.frames[cont]
        if cont.find("DTL_") == 0 or cont.find("Contabilitate") == 0:
            frame.Show(cont)
        frame.tkraise()



class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent,background="bisque")
        tk.Label(self, text="PHARMAPLUS", font=("Verdana", 20),background="bisque").pack(pady=20,padx=20)
        tk.Button(self, text="INITIALIZARE ",command=lambda: controller.show_frame('InitDataBase')).pack(pady = 20,padx = 20)
        tk.Button(self,text = "TRANZACTIE",command = lambda : controller.show_frame('Transaction')).pack(pady = 20,padx = 20)
        tk.Button(self,text = "ACTUALIZARE",command = lambda : controller.show_frame('ActualizareStoc')).pack(pady=20,padx=20)
        tk.Button(self,text = "CONTABILITATE",command = lambda: controller.show_frame('Contabilitate')).pack(pady=20,padx=20)
        tk.Button(self, text="AFISARE TABELE",command=lambda: controller.show_frame('DisplayTables')).pack(pady = 20,padx = 20)
        tk.Button(self, text="INCHIDERE", width=10, command=lambda:(database.connection.close(),exit(0))).pack(pady = 10,padx = 40)



class DBConnect(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent,background="bisque")

        tk.Label(self, text="Database Connect", font=("Verdana", 20),background="bisque").pack(pady=20,padx=20)
        tk.Label(self,text='Username',font=("Verdana", 18),background="bisque").pack(pady=20,padx=20)
        username = tk.Entry(self)
        username.pack(padx = 10)

        tk.Label(self,text='Password',font=("Verdana", 18),background="bisque").pack(pady=20,padx=20)
        password = tk.Entry(self,show='*')
        password.pack(padx = 10)

        tk.Button(self, text="CONECTARE",command=lambda: self.check(username.get(),password.get(),controller)).pack(pady = 20,padx = 20)
        tk.Button(self, text="INCHIDERE", width=10, command=exit).pack(pady = 40,padx = 40)

        self.status = tk.Label(self,font=("Verdana", 20),background="bisque")


    def check(self,user,password,controller):
        connecting_status = database.Connect(user,password)
        if connecting_status[0] == True:
            time.sleep(1/10)
            controller.show_frame('StartPage')
        else:
            self.status.pack_forget()
            self.status['text'] = '{} Incerca din nou!'.format(connecting_status[1])
            self.status.pack(pady=30,padx=20)



class InitDataBase(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,background="bisque")
        tk.Label(self,text="Initializare baza de date", font=("Verdana", 20),background="bisque").pack(padx=10,pady=20)
        tk.Label(self,text="Consola", font=("Verdana", 20),background="bisque").pack(padx=10,pady=20)
        self.terminal = tk.Text(self,width = 150,height = 30,background="tan1",foreground="black")
        self.terminal.pack(padx = 10,pady = 10)

        self.CreateTables()
        self.AddConstraints()
        self.TablesInsert()

        tk.Button(self, text="Mergi inapoi", width=10, command=lambda:controller.show_frame("StartPage")).pack(pady = 40,padx = 40)

    def CreateTables(self):
        self.terminal.insert(tk.END,'-' * self.terminal['width'] + "\n")
        time.sleep(1)
        message = "Table creation\n\n"
        self.terminal.insert(tk.END," " * (int(self.terminal['width']/2 - len(message)/2)) + message)
        for message in database.TablesCreation():
            self.terminal.insert(tk.END," " * (int(self.terminal['width']/2 - len(message)/2)) + message + "\n")
        self.terminal.insert(tk.END,"\n\n\n\n")

    def AddConstraints(self):
        message = "Table adding constraints\n\n"
        self.terminal.insert(tk.END," " * (int(self.terminal['width']/2 - len(message)/2)) + message)
        for message in database.AddConstraints():
            self.terminal.insert(tk.END," " * (int(self.terminal['width']/2 - len(message)/2)) + message + "\n")
        self.terminal.insert(tk.END,"\n\n\n\n")

    def TablesInsert(self):
        message = "Table insertions\n\n"
        self.terminal.insert(tk.END," " * (int(self.terminal['width']/2 - len(message)/2)) + message)
        for message in database.TableInsertions():
            self.terminal.insert(tk.END," " * (int(self.terminal['width']/2 - len(message)/2)) + message + "\n")



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



if __name__ == "__main__":
    app = GUI()
    app.mainloop()
