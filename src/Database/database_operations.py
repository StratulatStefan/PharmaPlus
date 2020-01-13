import cx_Oracle as Oracle


class DataBaseOperations:
    @staticmethod
    def CreateTable(cursor,tablename,fields):
        command = 'CREATE TABLE ' + tablename + '('
        for item in fields.items():
            command = command + item[0] + '  ' + item[1] + ', '
        command = command[:-2]
        command += ')'
        try:
            cursor.execute(command)
        except Oracle.DatabaseError:
            return "Table " + tablename + " already created!"
        else:
            return "Table " + tablename + " successufully created!"

    @staticmethod
    def AddConstraintPrimaryKey(cursor,table,attribute):
        command = 'ALTER TABLE ' + table + '\
               ADD CONSTRAINT ' + table[:5] + '_' + attribute[:5] +  '_PK PRIMARY KEY (' + attribute + ')'
        try:
            cursor.execute(command)
        except Oracle.DatabaseError:
            return "Constraint " + table[:5] + '_' + attribute[:5] + "_PK " + " already created!"
        else:
            return "Constraint " + table[:5] + '_' + attribute[:5] + "_PK " + " successfully created!"

    @staticmethod
    def AddConstraintForeignKey(cursor,table,foreigntable,attribute,foreignattribute):
        command = 'ALTER TABLE ' + table + '\
                   ADD CONSTRAINT ' + table[:5] + '_' + attribute[:5] + '_FK FOREIGN KEY (' + attribute + ' ) '+ \
                  'REFERENCES ' + foreigntable + ' (' + foreignattribute + ')'
        try:
            cursor.execute(command)
        except Oracle.DatabaseError:
            return "Constraint " + table[:5] + '_' + attribute[:5] + "_FK " + " already created!"
        else:
            return "Constraint " + table[:5] + '_' + attribute[:5] + "_FK " + " successfully created!"

    @staticmethod
    def AddConstraintUniqueKey(cursor,table,column_names):
        cls = ''
        for column in column_names:
            cls += column + ', '
        cls = cls[:-2]

        command = 'ALTER TABLE ' + table + '\
                   ADD CONSTRAINT ' + table + '_UK UNIQUE (' + cls + ')'
        try:
            cursor.execute(command)
        except Oracle.DatabaseError:
            return "Constraint " + table + "_UK " + " already created!"
        else:
            return "Constraint " + table + "_UK " + " successfully created!"

    @staticmethod
    def InsertCommand(connection,command):
        try:
            connection.cursor().execute(command)
            connection.commit()
        except Oracle.DatabaseError:
            return False, "Tuple {} already inserted!".format(command)
        else:
            return True, "Insertion successfully made!"

    @staticmethod
    def SelectAllFromTable(cursor,tablename):
        description = []
        list = []
        try:
            cursor.execute('SELECT * FROM ' + tablename)
            for row in cursor.description:
                description.append(row[0])
            for row in cursor.fetchall():
                tuple = {}
                for i in range(len(description)):
                    tuple.update({description[i] : row[i]})
                list.append(tuple)
        except Oracle.DatabaseError:
            return "Select * from " + tablename + " error!",list
        else:
            return "Select * from " + tablename + " done!",list

    @staticmethod
    def GetTableDescription(cursor,table):
        description = []
        try:
            cursor.execute('SELECT * FROM ' + table)
            for row in cursor.description:
                description.append(row[0])
        except Oracle.DatabaseError:
            print("Select * from " + table + " error!")
        else:
            print("Select * from " + table + " done!")
        return description

    @staticmethod
    def GetAllFromTable(cursor,table):
        list = []
        try:
            cursor.execute('SELECT * FROM ' + table)
            for row in cursor.fetchall():
                list.append(row)
        except Oracle.DatabaseError:
            print("Select * from " + table + " error!")
        else:
            print("Select * from " + table + " done!")
        return list

    @staticmethod
    def ExtractColumnsWithCondition(cursor,tablename,columns,condition):
        list = []
        cls = ""
        for column in columns:
            cls = cls + column + ", "
        cls = cls[:-2]
        command =  'SELECT ' + cls + ' FROM ' + tablename
        if condition != 0:
            command += " WHERE " + condition
        try:
            cursor.execute(command)
            for row in cursor.fetchall():
                list.append(row)
        except Oracle.DatabaseError:
            print("Could not fetch columns {} from {}.".format(cls,tablename))
        else:
            print("Columns {} successfully fetched!".format(cls))
        return list

    @staticmethod
    def ExtractEmployeesfromPharma(cursor,pharma):
        list = []
        command = "SELECT A.NUME_ANGAJAT,\
                          A.FUNCTIE,\
                          A.ID_ANGAJAT\
                   FROM FARMACII F, ANGAJATI A\
                   WHERE F.ID_FARMACIE = A.ID_FARMACIE AND\
                         A.FUNCTIE != 'MANAGER' AND\
                         F.ID_FARMACIE = {}\
                   ORDER BY A.ID_ANGAJAT".format(pharma)
        try:
            cursor.execute(command)
            for row in cursor.fetchall():
                list.append(row)
        except Oracle.DatabaseError:
            print("Could not fetch columns from joining.")
        else:
            print("Columns successfully fetched from joining!")
        return list

    @staticmethod
    def ExtractDrugsForSpecificEmployee(cursor,job_id):
        list = []
        command = "SELECT DISTINCT M.ID_MEDICAMENT,\
                                   M.NUME\
                   FROM MEDICAMENTE M, ANGAJATI A\
                   WHERE (M.CATEGORIE = 'intern' AND A.FUNCTIE = 'FARMACIST') OR\
                         ((M.CATEGORIE = 'liber' OR M.CATEGORIE = 'reteta') AND A.FUNCTIE = 'ASISTENT') AND\
                          A.FUNCTIE = '{}'\
                   ORDER BY M.ID_MEDICAMENT".format(job_id)
        try:
            cursor.execute(command)
            for row in cursor.fetchall():
                list.append(row)
        except Oracle.DatabaseError:
            print("Could not fetch columns from joining.")
        else:
            print("Columns successfully fetched from joining!")
        return list

    @staticmethod
    def ExtractDrugsInventory(cursor,pharma,drug):
        list = []
        command = "SELECT S.STOC,\
                          S.PRET_VANZARE\
                   FROM FARMACII F, STOCURI S,MEDICAMENTE M\
                   WHERE F.ID_FARMACIE = S.ID_FARMACIE AND\
                         M.ID_MEDICAMENT = S.ID_MEDICAMENT AND\
                         F.ID_FARMACIE = {} AND\
                         M.ID_MEDICAMENT = {}".format(pharma,drug)
        try:
            cursor.execute(command)
            for row in cursor.fetchall():
                list.append(row)
        except Oracle.DatabaseError:
            print("Could not fetch Stoc from joining.")
        else:
            print("Stoc successfully fetched from joining!")
        return list

    @staticmethod
    def AlterSales(connection,quantity,employee,drug):
        cursor = connection.cursor()
        command = "UPDATE VANZARI\
                   SET CANTITATE = CANTITATE + {}\
                   WHERE ID_ANGAJAT = {} AND ID_MEDICAMENT = {}".format(quantity,employee,drug)
        try:
            cursor.execute(command)
            connection.commit()
        except Oracle.DatabaseError:
            print("Could not alter table VANZARI")
        else:
            print("VANZARI successfully altered.")

    @staticmethod
    def AlterInventory(connection,quantity,pharma,drug):
        cursor = connection.cursor()
        command = "UPDATE STOCURI\
                   SET STOC = STOC - ({})\
                   WHERE ID_FARMACIE = {} AND ID_MEDICAMENT = {}".format(quantity,pharma,drug)
        try:
            cursor.execute(command)
            connection.commit()
        except Oracle.DatabaseError:
            print("Could not alter table STOCURI")
        else:
            print("STOCURI successfully altered.")

    @staticmethod
    def AlterDeposits(connection,quantity,drug,supplier):
        cursor = connection.cursor()
        command = "UPDATE DEPOZITE\
                   SET STOC = STOC - ({})\
                   WHERE ID_DISTRIBUITOR = {} AND ID_MEDICAMENT = {}".format(quantity,supplier,drug)
        try:
            cursor.execute(command)
            connection.commit()
        except Oracle.DatabaseError:
            print("Could not alter table DEPOZITE")
        else:
            print("DEPOZITE successfully altered.")

    @staticmethod
    def GetDrugNameFromDeposits(cursor,id_supplier):
        list = []
        command = "SELECT ID_MEDICAMENT,\
                          NUME\
                   FROM MEDICAMENTE\
                   WHERE ID_MEDICAMENT IN (SELECT ID_MEDICAMENT\
                                           FROM DEPOZITE\
                                           WHERE ID_DISTRIBUITOR = {})".format(id_supplier)
        try:
            cursor.execute(command)
            for row in cursor.fetchall():
                list.append(row)
        except Oracle.DatabaseError:
            print("Could not fetch Medicamente from joining.")
        else:
            print("Medicamente successfully fetched from joining!")
        return list

    @staticmethod
    def ExtractSoldQuantityPerPharma(cursor,pharma):
        command = 'SELECT SUM(CANTITATE) ' \
                  'FROM VANZARI ' \
                  'WHERE ID_ANGAJAT IN (SELECT ID_ANGAJAT ' \
                  'FROM ANGAJATI ' \
                  'WHERE ID_FARMACIE = {})'.format(pharma)
        list = []
        try:
            cursor.execute(command)
            for row in cursor.fetchall():
                list.append(row)
        except Oracle.DatabaseError:
            print("Select * from Vanzari error!")
        else:
            print("Select * from Vanzari done!")
        return list

    @staticmethod
    def ExtractSalesStatus(cursor,pharma):
        command = 'SELECT V.ID_ANGAJAT, ' \
                  'V.CANTITATE, ' \
                  'V.ID_MEDICAMENT, ' \
                  'S.PRET_VANZARE * V.CANTITATE ' \
                  'FROM VANZARI V, STOCURI S ' \
                  'WHERE S.ID_MEDICAMENT = V.ID_MEDICAMENT AND ' \
                  'S.ID_FARMACIE = {} AND ' \
                  'V.ID_ANGAJAT IN (SELECT ID_ANGAJAT ' \
                  'FROM ANGAJATI ' \
                  'WHERE ID_FARMACIE = {})' \
                  ''.format(pharma,pharma)
        list = []
        try:
            cursor.execute(command)
            for row in cursor.fetchall():
                list.append(row)
        except Oracle.DatabaseError:
            print("Select * from Vanzari,Stocuri error!")
        else:
            print("Select * from Vanzari,Stocuri done!")
        return list

    @staticmethod
    def ExtractGrossPrice(cursor,pharma):
        command = 'SELECT V.ID_ANGAJAT, ' \
                  'V.CANTITATE, ' \
                  'V.ID_MEDICAMENT, ' \
                  'M.PRET_IMPUS * V.CANTITATE ' \
                  'FROM VANZARI V, MEDICAMENTE M ' \
                  'WHERE M.ID_MEDICAMENT = V.ID_MEDICAMENT AND ' \
                  'V.ID_ANGAJAT IN (SELECT ID_ANGAJAT ' \
                  'FROM ANGAJATI ' \
                  'WHERE ID_FARMACIE = {})' \
                  ''.format(pharma,pharma)
        list = []
        try:
            cursor.execute(command)
            for row in cursor.fetchall():
                list.append(row)
        except Oracle.DatabaseError:
            print("Select * from Vanzari,Stocuri error!")
        else:
            print("Select * from Vanzari,Stocuri done!")
        return list
