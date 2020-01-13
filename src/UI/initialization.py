import tkinter as tk
import time
from Database.database import *


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