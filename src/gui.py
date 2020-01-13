from UI.transaction import *
from UI.store_update import *
from UI.accounting import *
from UI.display_tables import *
from UI.initialization import *



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


if __name__ == "__main__":
    app = GUI()
    app.mainloop()
