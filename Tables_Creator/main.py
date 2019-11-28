import cx_Oracle as Oracle
import random as rand
import math

TVA = 5
printlist = lambda x : [print(element) for element in x]

def AddConstraintPrimaryKey(table,attribute):
    command = 'ALTER TABLE ' + table + '\
               ADD CONSTRAINT ' + table + '_' + attribute + '_PK PRIMARY KEY (' + attribute + ')'
    try:
        cursor.execute(command)
    except Oracle.DatabaseError:
        print("Constraint " + table + "_" + attribute + "_PK " + " already created!")
    else:
        print("Constraint " + table + "_" + attribute + "_PK " + " successfully added!")

def AddConstraintForeignKey(table,foreigntable,attribute,foreignattribute):
    command = 'ALTER TABLE ' + table + '\
               ADD CONSTRAINT ' + table + '_' + attribute + '_FK FOREIGN KEY (' + attribute + ' ) '+\
              'REFERENCES ' + foreigntable + ' (' + foreignattribute + ')'
    try:
        cursor.execute(command)
    except Oracle.DatabaseError:
        print("Constraint " + table + "_" + attribute + "_FK " + " already created!")
    else:
        print("Constraint " + table + "_" + attribute + "_FK " + " successfully added!")

def AddConstraintUniqueKey(table,column_names):
    cls = ''
    for column in column_names:
        cls += column + ', '
    cls = cls[:-2]
    print(cls)

    command = 'ALTER TABLE ' + table + '\
               ADD CONSTRAINT ' + table + '_UK UNIQUE (' + cls + ')'

    try:
        cursor.execute(command)
    except Oracle.DatabaseError:
        print("Constraint " + table + "_UK " + " already created!")
    else:
        print("Constraint " + table + "_UK " + " successfully added!")

def InsertCommand(command):
    #print(command)
    try:
        cursor.execute(command)
        connection.commit()
    except Oracle.DatabaseError:
        i = 10
        #print("Already inserted!")
    else:
        print("Insertion successfully made!")

def CreateTable(tablename,fields):
    command = 'CREATE TABLE ' + tablename + '('
    for item in fields.items():
        command = command + item[0] + '  '+ item[1] + ', '
    command = command[:-2]
    command += ')'

    try:
        cursor.execute(command)
    except Oracle.DatabaseError:
        print("Table " + tablename + " already created!")
    else:
        print("Table " + tablename +" successufully created!")

def TablesCreation():

    locationsmap = {
        "ID_LOCATIE"  : "NUMBER(6)      NOT NULL",
        "STRADA"      : "VARCHAR2(30)   NOT NULL",
        "NUMAR"       : "NUMBER(3)      NOT NULL",
        "ORAS"        : "VARCHAR2(10)   NOT NULL"
    }
    CreateTable('LOCATIi',locationsmap)



    employeesmap = {
        "ID_FARMACIE"     : "NUMBER(6)     NOT NULL",
        "ID_ANGAJAT "     : "NUMBER(6)     NOT NULL",
        "NUME_ANGAJAT"    : "VARCHAR2(30)  NOT NULL",
        "FUNCTIE"         : "VARCHAR2(10)  NOT NULL",
        "SALARIU"         : "NUMBER(5)     NOT NULL",
        "DATA_ANGAJARII"  : "DATE          NOT NULL"
    }
    CreateTable("ANGAJATI",employeesmap)



    medicamentmap = {
        "ID_MEDICAMENT" : "NUMBER(10)   NOT NULL",
        "NUME"          : "VARCHAR2(15) NOT NULL",
        "CATEGORIE"     : "VARCHAR2(20) NOT NULL",
        "PRET_IMPUS"    : "NUMBER(4,2)  NOT NULL"
    }
    CreateTable("MEDICAMENTE",medicamentmap)



    farmaciemap = {
        "ID_FARMACIE"     : "NUMBER(6)  NOT NULL",
        "ID_LOCATIE"      : "NUMBER(6)  NOT NULL",
        "ID_MANAGER"      : "NUMBER(6)  NOT NULL",
        "ADAOS_IMPUS"     : "NUMBER(6)  NOT NULL",
        "ID_DISTRIBUITOR" : "NUMBER(3)  NOT NULL"
    }
    CreateTable("FARMACII",farmaciemap)



    stocurimap = {
        "ID_FARMACIE "   : "NUMBER(6)    NOT NULL",
        "ID_MEDICAMENT"  : "NUMBER(10)   NOT NULL",
        "STOC"           : "NUMBER(5)    NOT NULL",
        "PRET_VANZARE"   : "NUMBER(5,2)  NOT NULL"
    }
    CreateTable("STOCURI",stocurimap)



    distribuitorimap = {
        "ID_DISTRIBUITOR" :  "NUMBER(3)     NOT NULL",
        "NUME"            :  "VARCHAR2(15)  NOT NULL",
    }
    CreateTable("DISTRIBUITORI",distribuitorimap)


    depozitmap = {
        "ID_DISTRIBUITOR " : "NUMBER(3)   NOT NULL",
        "ID_MEDICAMENT"    : "NUMBER(10)  NOT NULL",
        "STOC"             : "NUMBER(6)   NOT NULL",
        "PRET"             : "NUMBER(5,2) NOT NULL"

    }
    CreateTable("DEPOZITE",depozitmap)

    vanzarimap = {
        "ID_ANGAJAT"    :  "NUMBER(6) NOT NULL",
        "ID_MEDICAMENT" : "NUMBER(10) NOT NULL",
        "CANTITATE"     : "NUMBER(5)  NOT NULL"
    }
    CreateTable("VANZARI",vanzarimap)

def Connection():
    connection_done = False
    while connection_done == False:
       # username = input("Username : ")
       # password = input("Password : ")
        username = "PHARMA"
        password = "8246"
        try:
            connection = Oracle.connect(username,password,"localhost/xe")
            connection_done = True
            print("Connection successfully done!\n")

        except Oracle.DatabaseError:
            print("Wrong username or password! Try again!")
    return connection

def AddConstraints():
    AddConstraintPrimaryKey('LOCATII',       'ID_LOCATIE')
    AddConstraintPrimaryKey('ANGAJATI',      'ID_ANGAJAT')
    AddConstraintPrimaryKey('MEDICAMENTE',   'ID_MEDICAMENT')
    AddConstraintPrimaryKey('FARMACII',      'ID_FARMACIE')
    AddConstraintPrimaryKey('DISTRIBUITORI', 'ID_DISTRIBUITOR')
    print()
    AddConstraintForeignKey('FARMACII',      'LOCATII',       'ID_LOCATIE',      'ID_LOCATIE')
    AddConstraintForeignKey('STOCURI',       'MEDICAMENTE',   'ID_MEDICAMENT',   'ID_MEDICAMENT')
    AddConstraintForeignKey('DEPOZITE',      'MEDICAMENTE',   'ID_MEDICAMENT',   'ID_MEDICAMENT')
    AddConstraintForeignKey('ANGAJATI',      'FARMACII',      'ID_FARMACIE',     'ID_FARMACIE')
    AddConstraintForeignKey('VANZARI',       'ANGAJATI',      'ID_ANGAJAT',      'ID_ANGAJAT')
    AddConstraintForeignKey('FARMACII',      'DISTRIBUITORI',  'ID_DISTRIBUITOR','ID_DISTRIBUITOR')
    AddConstraintForeignKey('STOCURI',       'FARMACII',      'ID_FARMACIE',     'ID_FARMACIE')
    AddConstraintForeignKey('DEPOZITE',      'DISTRIBUITORI', 'ID_DISTRIBUITOR', 'ID_DISTRIBUITOR')
    print()
    AddConstraintUniqueKey('VANZARI',['ID_ANGAJAT','ID_MEDICAMENT'])
    AddConstraintUniqueKey('STOCURI',['ID_FARMACIE','ID_MEDICAMENT'])
    AddConstraintUniqueKey('DEPOZITE',['ID_DISTRIBUITOR','ID_MEDICAMENT'])

def SelectAllFromTable(table):
    list = []
    description = []
    try:
        cursor.execute('SELECT * FROM ' + table)
        for row in cursor.description:
            description.append(row[0])
        for row in cursor.fetchall():
            tuple = {}
            for i in range(len(description)):
                tuple.update({description[i] : row[i]})
            list.append(tuple)
    except Oracle.DatabaseError:
        print("Select * from " + table + " error!")
    else:
        print("Select * from " + table + " done!")
    return list

def TableInsertions():
    locations = [(1000, 'Dimitrie Leonida',  12,  'IASI'),
                 (1010, 'Stefan cel Mare',   4,   'BUCURESTI'),
                 (1020, 'Independentei',     10,  'CLUJ')
    ]
    for row in locations:
        InsertCommand('INSERT INTO LOCATII VALUES {}'.format(row))


    farmacii = [(2000,  1000,  100,    15,  600),
                (2001,  1010,  150,    10,  720),
                (2002,  1020,  300,    12,  600)
    ]
    for row in farmacii:
        InsertCommand('INSERT INTO FARMACII VALUES {}'.format(row))


    medicamente = [(100,  'Paracetamol',     'liber' ,  1.2),
                   (101,  'Aspirina',        'liber',   8),
                   (102,  'Penicilina',      'reteta',  30),
                   (103,  'Amoxacilina',     'reteta',  5.5),
                   (104,  'Theraflu',        'liber',   2),
                   (105,  'Decasept',        'liber',   7),
                   (106,  'Aulin',           'liber',   15),
                   (107,  'Augmentin',       'reteta',  20.4),
                   (108,  'Acamol',          'reteta',  21),
                   (109,  'Sinecod',         'reteta',  18.3),
                   (110,  'Bioflu',          'liber',   5),
                   (111,  'Metoclopramid',   'liber',   7),
                   (112,  'NO-SPA',          'liber',   9.1),
                   (113,  'Dulcolax',        'reteta',  11),
                   (114,  'Linex',           'reteta',  15.5),
                   (115,  'Gaviscon',        'reteta',  30),
                   (116,  'Redigest',        'liber',   4.2),
                   (117,  'Dicarbocalm',     'liber',   5),
                   (118,  'Voltaren',        'reteta',  12),
                   (119,  'Aflamil',         'reteta',  18.9),
                   (120,  'Nitromint',       'reteta',  20),
                   (121,  'Olicard',         'reteta',  12),
                   (122,  'Tertensif',       'liber',   50.7),
                   (123,  'Sermion',         'reteta',  11),
                   (124,  'Betaloc',         'reteta',  7),
                   (125,  'Tador',           'liber',   10.2),
                   (126,  'Glicerina',       'intern',  15),
                   (127,  'Ceai',            'intern',  6),
                   (128,  'Crema',           'intern',  20),
                   (129,  'Tinctura',        'intern',  30),
                   (130,  'Unguent',         'intern',  40)
    ]
    for row in medicamente:
        InsertCommand('INSERT INTO MEDICAMENTE VALUES {}'.format(row))


    angajati = [(2000,  100,  'Popescu Ioan',      'MANAGER',   6000,  '24-APR-13'),
                (2000,  110,  'Andries Maria',     'FARMACIST', 4500,  '28-APR-13'),
                (2000,  125,  'Matei Alexandru',   'FARMACIST', 4200,  '5-MAY-13'),
                (2000,  120,  'Baltag Cosmin',     'ASISTENT',  3000,  '5-MAY-13'),
                (2000,  135,  'Atomei Maria',      'ASISTENT',  3200,  '5-MAY-13'),
                (2000,  138,  'Apetrei Diana',     'ASISTENT',  3100,  '8-MAY-13'),

                (2001,  150,  'Gavrilescu Adrian', 'MANAGER',   10000, '12-DEC-15'),
                (2001,  160,  'Bejan Mihai',       'FARMACIST', 5500,  '13-DEC-15'),
                (2001,  165,  'Stanciu Eduard',    'FARMACIST', 6000,  '13-DEC-15'),
                (2001,  170,  'Platon Magda',      'ASISTENT',  4000,  '14-DEC-15'),
                (2001,  175,  'Zaharia Andreea',   'ASISTENT',  4200,  '16-DEC-15'),
                (2001,  178,  'Gherasim Ioana',    'ASISTENT',  4400,  '21-DEC-15'),

                (2002,  300,  'Ionescu Marian',    'MANAGER',   8000,  '1-AUG-18'),
                (2002,  310,  'Aioanei Adela',     'FARMACIST', 5000,  '2-AUG-18'),
                (2002,  315,  'Tanasa Ana',        'FARMACIST', 4500,  '15-AUG-18'),
                (2002,  320,  'Sava Bianca',       'ASISTENT',  3500,  '4-AUG-18'),
                (2002,  325,  'Florea Georgia',    'ASISTENT',  3800,  '12-AUG-18'),
                (2002,  328,  'Rosu Maria',        'ASISTENT',  3400,  '30-AUG-18'),
    ]
    for row in angajati:
        InsertCommand('INSERT INTO ANGAJATI VALUES {}'.format(row))

    stocuri = []
    farmacii = SelectAllFromTable('FARMACII')
    medicamente = SelectAllFromTable('MEDICAMENTE')
    for farmacie in farmacii:
        id_farmacie = farmacie['ID_FARMACIE']
        adaos_farmacie = farmacie['ADAOS_IMPUS']
        for medicament in medicamente:
            tip_medicament = medicament['CATEGORIE']
            id_medicament = medicament['ID_MEDICAMENT']
            pret_medicament = medicament['PRET_IMPUS']
            stoc = rand.randrange(100,300)
            if tip_medicament == 'intern':
                pret_vanzare = pret_medicament + pret_medicament * adaos_farmacie/100
            else:
                pret_vanzare = pret_medicament + pret_medicament * (adaos_farmacie+TVA)/100
            stocuri.append((id_farmacie,id_medicament,stoc,pret_vanzare))
    for row in stocuri:
        InsertCommand('INSERT INTO STOCURI VALUES {}'.format(row))


    vanzari = []
    angajati = SelectAllFromTable('ANGAJATI')
    for angajat in angajati:
        functie_angajat =  angajat['FUNCTIE']
        id_angajat = angajat['ID_ANGAJAT']
        for medicament in medicamente:
            tip_medicament = medicament['CATEGORIE']
            id_medicament = medicament['ID_MEDICAMENT']
            if functie_angajat == 'ASISTENT' and tip_medicament != 'intern':
                vanzari.append((id_angajat,id_medicament,0))
            elif functie_angajat == 'FARMACIST' and tip_medicament == 'intern':
                vanzari.append((id_angajat,id_medicament,0))
    for row in vanzari:
        InsertCommand('INSERT INTO VANZARI VALUES {}'.format(row))


    distribuitori = [(600,  'Farmexpert'),
                     (720,  'Mediplus')
    ]
    for roww in distribuitori:
        print(roww)
        InsertCommand('INSERT INTO DISTRIBUITORI VALUES {}'.format(roww))

    distr = SelectAllFromTable('DISTRIBUITORI')
    medicamente = SelectAllFromTable('MEDICAMENTE')
    depozite = []
    for depozit in distr:
        id_depozit = depozit['ID_DISTRIBUITOR']
        for medicament in medicamente:
            id_medicament = medicament['ID_MEDICAMENT']
            pret_medicament = medicament['PRET_IMPUS']
            tip_medicament = medicament['CATEGORIE']
            pret_vanzare = pret_medicament + pret_medicament * 5/100
            if tip_medicament != 'intern':
                depozite.append((id_depozit,id_medicament,rand.randrange(1000,2000),pret_vanzare))
    for row in depozite:
        InsertCommand('INSERT INTO DEPOZITE VALUES {}'.format(row))


if __name__ == "__main__":
    connection = Connection()
    print('--------------------------------')
    cursor = connection.cursor()
    TablesCreation()
    print('--------------------------------')
    AddConstraints()
    print('--------------------------------')
    print()
    TableInsertions()
    connection.close()

