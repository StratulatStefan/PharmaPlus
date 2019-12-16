import random as rand
import TablesFormat as tformat
from database_operations import *

username = input("Username : ")
password = input("Password : ")

class DataBaseConnection:
    def __init__(self):
        self.username = None
        self.password = None
        self.server_address = "localhost/xe"
        self.connection = None

    def authentification(self,user,passw):
        if user.lower() == username:
            self.username = user
        else:
            return False, "Username gresit!\n"
        if passw.lower() == password:
            self.password = passw
        else:
            return False, "Parola gresita!\n"

        self.connection = Oracle.connect(self.username,self.password,self.server_address)
        return True, "Conectare realizata cu succes!\n"

    def close(self):
        self.connection.connection.close()

    def commit(self):
        self.connection.commit()

    def cursor(self):
        return self.connection.cursor()

class DataBase:
    def __init__(self):
        self.connection = DataBaseConnection()
        self.connection.authentification(username,password)
        self.cursor_ = self.connection.connection.cursor()

    def Connect(self,user,passw):
        conn = DataBaseConnection()
        status = conn.authentification(user,passw)
        if status[0] == True:
            self.connection = conn.connection
        return status

    def TablesCreation(self):
        yield DataBaseOperations.CreateTable(self.cursor_,'LOCATII',tformat.locations_map)
        yield DataBaseOperations.CreateTable(self.cursor_,"ANGAJATI",tformat.employees_map)
        yield DataBaseOperations.CreateTable(self.cursor_,"MEDICAMENTE",tformat.drugs_map)
        yield DataBaseOperations.CreateTable(self.cursor_,"FARMACII",tformat.pharmas_map)
        yield DataBaseOperations.CreateTable(self.cursor_,"STOCURI",tformat.inventories_map)
        yield DataBaseOperations.CreateTable(self.cursor_,"DISTRIBUITORI",tformat.suppliers_map)
        yield DataBaseOperations.CreateTable(self.cursor_,"DEPOZITE",tformat.deposits_map)
        yield DataBaseOperations.CreateTable(self.cursor_,"VANZARI",tformat.sales_map)

    def AddConstraints(self):
        for element in tformat.primary_key:
            yield DataBaseOperations.AddConstraintPrimaryKey(self.cursor_,element[0],element[1])

        yield "\n"

        for element in tformat.foreign_key:
            yield DataBaseOperations.AddConstraintForeignKey(self.cursor_,element[0],element[1],element[2],element[3])

        yield "\n"

        for element in tformat.unique_key:
            yield DataBaseOperations.AddConstraintUniqueKey(self.cursor_,element[0],element[1])

    def TableInsertions(self):
        for row in tformat.locations:
            yield DataBaseOperations.InsertCommand(self.connection,'INSERT INTO LOCATII VALUES {}'.format(row))[1]

        for row in tformat.pharmas:
            yield DataBaseOperations.InsertCommand(self.connection,'INSERT INTO FARMACII VALUES {}'.format(row))[1]

        for row in tformat.drugs:
            yield DataBaseOperations.InsertCommand(self.connection,'INSERT INTO MEDICAMENTE VALUES {}'.format(row))[1]

        for row in tformat.employees:
            yield DataBaseOperations.InsertCommand(self.connection,'INSERT INTO ANGAJATI VALUES {}'.format(row))[1]


        inventories = []
        pharmas = DataBaseOperations.SelectAllFromTable(self.cursor_,'FARMACII')[1]
        drugs = DataBaseOperations.SelectAllFromTable(self.cursor_,'MEDICAMENTE')[1]
        for pharma in pharmas:
            id_pharma = pharma['ID_FARMACIE']
            adaos_pharma = pharma['ADAOS_IMPUS']
            for med in drugs:
                drug_type = med['CATEGORIE']
                id_drug = med['ID_MEDICAMENT']
                drug_price = med['PRET_IMPUS']
                inventory = rand.randrange(100,300)
                if drug_type == 'intern':
                    sale_price = drug_price + drug_price * adaos_pharma/100
                else:
                    sale_price = drug_price + drug_price * (adaos_pharma + tformat.TVA)/100
                inventories.append((id_pharma,id_drug,inventory,sale_price))
        for row in inventories:
            yield DataBaseOperations.InsertCommand(self.connection,'INSERT INTO STOCURI VALUES {}'.format(row))[1]


        for roww in tformat.suppliers:
            DataBaseOperations.InsertCommand(self.connection,'INSERT INTO DISTRIBUITORI VALUES {}'.format(roww))[1]

        suppliers = DataBaseOperations.SelectAllFromTable(self.cursor_,'DISTRIBUITORI')[1]
        drugs = DataBaseOperations.SelectAllFromTable(self.cursor_,'MEDICAMENTE')[1]
        deposits = []
        for deposit in suppliers:
            id_deposit = deposit['ID_DISTRIBUITOR']
            for drug in drugs:
                id_drug = drug['ID_MEDICAMENT']
                drug_price = drug['PRET_IMPUS']
                drug_type = drug['CATEGORIE']
                sale_price = drug_price + drug_price * 5/100
                if drug_type != 'intern':
                    deposits.append((id_deposit,id_drug,rand.randrange(1000,2000),sale_price))
        for row in deposits:
            yield DataBaseOperations.InsertCommand(self.connection,'INSERT INTO DEPOZITE VALUES {}'.format(row))[1]

        self.connection.connection.commit()
