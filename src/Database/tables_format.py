
#Formatul tabelelor

locations_map = {
    "ID_LOCATIE"  : "NUMBER(6)      NOT NULL",
    "STRADA"      : "VARCHAR2(30)   NOT NULL",
    "NUMAR"       : "NUMBER(3)      NOT NULL",
    "ORAS"        : "VARCHAR2(10)   NOT NULL"
}

employees_map = {
    "ID_FARMACIE"     : "NUMBER(6)     NOT NULL",
    "ID_ANGAJAT "     : "NUMBER(6)     NOT NULL",
    "NUME_ANGAJAT"    : "VARCHAR2(30)  NOT NULL",
    "FUNCTIE"         : "VARCHAR2(10)  NOT NULL",
    "SALARIU"         : "NUMBER(5)     NOT NULL",
    "DATA_ANGAJARII"  : "DATE          NOT NULL"
}

drugs_map = {
    "ID_MEDICAMENT" : "NUMBER(10)   NOT NULL",
    "NUME"          : "VARCHAR2(15) NOT NULL",
    "CATEGORIE"     : "VARCHAR2(20) NOT NULL",
    "PRET_IMPUS"    : "NUMBER(4,2)  NOT NULL"
}

pharmas_map = {
    "ID_FARMACIE"     : "NUMBER(6)  NOT NULL",
    "ID_LOCATIE"      : "NUMBER(6)  NOT NULL",
    "ID_MANAGER"      : "NUMBER(6)  NOT NULL",
    "ADAOS_IMPUS"     : "NUMBER(6)  NOT NULL",
    "ID_DISTRIBUITOR" : "NUMBER(3)  NOT NULL"
}

inventories_map = {
    "ID_FARMACIE "   : "NUMBER(6)    NOT NULL",
    "ID_MEDICAMENT"  : "NUMBER(10)   NOT NULL",
    "STOC"           : "NUMBER(5)    NOT NULL",
    "PRET_VANZARE"   : "NUMBER(5,2)  NOT NULL"
}

suppliers_map = {
    "ID_DISTRIBUITOR" :  "NUMBER(3)     NOT NULL",
    "NUME"            :  "VARCHAR2(15)  NOT NULL"
}

deposits_map = {
    "ID_DISTRIBUITOR " : "NUMBER(3)   NOT NULL",
    "ID_MEDICAMENT"    : "NUMBER(10)  NOT NULL",
    "STOC"             : "NUMBER(6)   NOT NULL",
    "PRET"             : "NUMBER(5,2) NOT NULL"
}

sales_map = {
    "ID_ANGAJAT"    :  "NUMBER(6) NOT NULL",
    "ID_MEDICAMENT" : "NUMBER(10) NOT NULL",
    "CANTITATE"     : "NUMBER(5)  NOT NULL"
}



#constrangeri

primary_key = [
    ['LOCATII',       'ID_LOCATIE'],
    ['ANGAJATI',      'ID_ANGAJAT'],
    ['DISTRIBUITORI', 'ID_DISTRIBUITOR'],
    ['MEDICAMENTE',   'ID_MEDICAMENT'],
    ['FARMACII',      'ID_FARMACIE']
]

foreign_key = [
    ['FARMACII',      'LOCATII',       'ID_LOCATIE',      'ID_LOCATIE'],
    ['STOCURI',       'MEDICAMENTE',   'ID_MEDICAMENT',   'ID_MEDICAMENT'],
    ['DEPOZITE',      'MEDICAMENTE',   'ID_MEDICAMENT',   'ID_MEDICAMENT'],
    ['ANGAJATI',      'FARMACII',      'ID_FARMACIE',     'ID_FARMACIE'],
    ['VANZARI',       'ANGAJATI',      'ID_ANGAJAT',      'ID_ANGAJAT'],
    ['FARMACII',      'DISTRIBUITORI',  'ID_DISTRIBUITOR','ID_DISTRIBUITOR'],
    ['STOCURI',       'FARMACII',      'ID_FARMACIE',     'ID_FARMACIE'],
    ['DEPOZITE',      'DISTRIBUITORI', 'ID_DISTRIBUITOR', 'ID_DISTRIBUITOR']
]

unique_key = [
    ['VANZARI',  ['ID_ANGAJAT','ID_MEDICAMENT']],
    ['STOCURI',  ['ID_FARMACIE','ID_MEDICAMENT']],
    ['DEPOZITE', ['ID_DISTRIBUITOR','ID_MEDICAMENT']]
]



#insert-uri


locations = [
    (1000, 'Dimitrie Leonida',  12,  'IASI'),
    (1010, 'Stefan cel Mare',   4,   'BUCURESTI'),
    (1020, 'Independentei',     10,  'CLUJ')
]

pharmas = [
    (2000,  1000,  100,    15,  600),
    (2001,  1010,  150,    10,  720),
    (2002,  1020,  300,    12,  600)
]

drugs = [
    (100,  'Paracetamol',     'liber' ,  1.2),
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

employees = [
    (2000,  100,  'Popescu Ioan',      'MANAGER',   6000,  '24-APR-13'),
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
    (2002,  328,  'Rosu Maria',        'ASISTENT',  3400,  '30-AUG-18')
]

suppliers = [
    (600,  'Farmexpert'),
    (720,  'Mediplus')]


TVA = 5
costs = [0,0,0]