import pyodbc
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi
from cryptography.fernet import Fernet
import sys
from os import path
from PyQt5.uic import loadUiType

cipher_key = b'APM1JDVgT8WDGOWBgQv6EIhvxl4vDYvUnVdg-Vjdt0o='
cipher = Fernet(cipher_key)
FORM_CLASS, _ = loadUiType(path.join(path.dirname('__file__'), "mainwindow.ui"))
server = 'LIGHTFLIGHTPC'
database = 'Coursework'
username = 'Course'
password = 'Course'
cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)


class Login(QDialog):

    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.login_btn.clicked.connect(self.LOGIN)
        self.pwd_line.setEchoMode(QtWidgets.QLineEdit.Password)

    def LOGIN(self):
        login = "'" + self.login_line.text() + "'"
        password = self.pwd_line.text()
        cursor = cnxn.cursor()
        pwd = "'" + cipher.encrypt(password.encode('utf-8')).decode('utf-8') + "'"
        query = "select * from Worker where WorkerLogin =" + login
        data = cursor.execute(query)
        test = cursor.fetchall()
        origin_pas = cipher.decrypt(test[0][7].encode('utf-8'))
        if len(test) > 0 and (str(origin_pas.decode("utf-8")) == password):
            self.cams = Main(test[0][4])
            self.cams.show()
            self.close()
        else:
            self.warning("Wrong login/password or account doesn't exist")

    def warning(self, message):
        mess = QtWidgets.QMessageBox()
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec_()


class Main(QMainWindow, FORM_CLASS):
    def __init__(self, prior, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons()
        self.prior = prior

    def Handel_Buttons(self):
        self.Tables_combobox.activated.connect(self.COMBOBOX)
        self.Queries_combobox.activated.connect(self.QUERIES)
        self.Views_combobox.activated.connect(self.VIEWS)
        self.deleteButton.clicked.connect(self.DELETE)
        self.updateButton.clicked.connect(self.UPDATE)
        self.addButton.clicked.connect(self.ADDPREP)

    def VIEWS(self):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        cursor = cnxn.cursor()
        value = self.Views_combobox.currentText()
        if value == "Cписок деталей и количество запросов на них":
            command = "select * from Detail_count_and_requests"
            self.tableWidget.setHorizontalHeaderLabels(["DetailName", "Count", "", "", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "Наиболее востребованная услуга по месяцам":
            command = "select * from most_needed_service_by_month"
            self.tableWidget.setHorizontalHeaderLabels(["ServiceName", "Count", "DateCreate", "", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "Зарплаты работников за месяц на основе отработанных часов":
            command = "select * from Workers_salary"
            self.tableWidget.setHorizontalHeaderLabels(["WorkerName", "Cost", "", "", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def ADD(self):
        cursor = cnxn.cursor()
        data = []
        value = self.Tables_combobox.currentText()
        if value == "Car":
            for column in range(3):
                test = self.tableWidget.item(0, column).text()
                data.append(test)
            command = "insert into Car values (" + data[0] + ",'" + data[1] + "', '" + data[2] + "')"
            cursor.execute(command)
            cnxn.commit()
            self.addButton.setText("Add new")
            self.COMBOBOX()
        if value == "Client":
            for column in range(4):
                test = self.tableWidget.item(0, column).text()
                data.append("'" + test + "'")
            command = "insert into Client values (" + data[0] + ", " + data[1] + ", " + data[2] + ", " + data[3] + ") "
            cursor.execute(command)
            cnxn.commit()
            self.addButton.setText("Add new")
            self.COMBOBOX()
        if value == "Details":
            for column in range(3):
                test = self.tableWidget.item(0, column).text()
                data.append("'" + test + "'")
            command = "insert into Details values ('" + data[0] + "', " + data[1] + ", " + data[2] + ") "
            cursor.execute(command)
            cnxn.commit()
            self.addButton.setText("Add new")
            self.COMBOBOX()
        if value == "DetailsList":
            for column in range(3):
                test = self.tableWidget.item(0, column).text()
                data.append(test)
            command = "insert into DetailsList values (" + data[0] + ", " + data[1] + ", " + data[2] + ")"
            cursor.execute(command)
            cnxn.commit()
            self.addButton.setText("Add new")
            self.COMBOBOX()
        if value == "DetailsRequest":
            for column in range(2):
                test = self.tableWidget.item(0, column).text()
                data.append(test)
            command = "insert into DetailsRequest values (" + data[0] + ", " + data[1] + ")"
            cursor.execute(command)
            cnxn.commit()
            self.addButton.setText("Add new")
            self.COMBOBOX()
        if value == "Orders":
            for column in range(4):
                test = self.tableWidget.item(0, column).text()
                data.append(test)
            command = "insert into Orders values (" + data[0] + ", '" + data[1] + "', '" + data[2] + "', " + data[3] + ")"
            cursor.execute(command)
            cnxn.commit()
            self.addButton.setText("Add new")
            self.COMBOBOX()
        if value == "ServiceList":
            for column in range(3):
                test = self.tableWidget.item(0, column).text()
                data.append(test)
            command = "insert into ServiceList values (" + data[0] + ", " + data[1] + ", " + data[2] + ")"
            cursor.execute(command)
            cnxn.commit()
            self.addButton.setText("Add new")
            self.COMBOBOX()
        if value == "Service":
            for column in range(2):
                test = self.tableWidget.item(0, column).text()
                data.append(test)
            command = "insert into Servise values (" + data[0] + ", " + data[1] + ")"
            cursor.execute(command)
            cnxn.commit()
            self.addButton.setText("Add new")
            self.COMBOBOX()
        if value == "Statuses":
            for column in range(1):
                test = self.tableWidget.item(0, column).text()
                data.append(test)
            command = "insert into Statuses values ('" + data[0] + "')"
            cursor.execute(command)
            cnxn.commit()
            self.addButton.setText("Add new")
            self.COMBOBOX()
        if value == "TimeSheet":
            for column in range(3):
                test = self.tableWidget.item(0, column).text()
                data.append(test)
            command = "insert into TimeSheet values (" + data[0] + ", " + data[1] + ", " + data[2] + ")"
            cursor.execute(command)
            cnxn.commit()
            self.addButton.setText("Add new")
            self.COMBOBOX()
        if value == "Worker":
            if self.prior == "Admin":
                for column in range(7):
                    test = self.tableWidget.item(0, column).text()
                    data.append(test)
                pwd = cipher.encrypt(data[6].encode('utf-8')).decode('utf-8')
                command = "exec add_worker '" + data[0] + "', '" + data[1] + "', '" + data[2] + "', '" + data[3] + "', " + data[4] + ", '" + data[5] + "', '" + data[6] + "' "
                cursor.execute(command)
                cnxn.commit()
                self.addButton.setText("Add new")
                self.COMBOBOX()
            else:
                mess = QtWidgets.QMessageBox()
                mess.setText("Access denied!")
                mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
                mess.exec_()
                self.addButton.setText("Add new")
                self.COMBOBOX()

    def ADDPREP(self):
        if self.addButton.text() == "Confirm":
            self.addButton.clicked.connect(self.ADD)
        else:
            self.tableWidget.clear()
            self.tableWidget.setRowCount(1)
            value = self.Tables_combobox.currentText()
            self.addButton.setText("Confirm")
            if value == "Car":
                self.tableWidget.setHorizontalHeaderLabels(["idClient", "Model", "Plate", "", "", ""])
            if value == "Client":
                self.tableWidget.setHorizontalHeaderLabels(["ClientName", "ClientSurname", "BirthDate", "Phone", "", ""])
            if value == "Details":
                self.tableWidget.setHorizontalHeaderLabels(["DetailName", "DetailCost", "DetailCount", "", "", ""])
            if value == "DetailsList":
                self.tableWidget.setHorizontalHeaderLabels(["idDetail", "DetailCount", "idRequest", "", "", ""])
            if value == "DetailsRequest":
                self.tableWidget.setHorizontalHeaderLabels(["idStatus", "idServiceList", "", "", "", ""])
            if value == "Orders":
                self.tableWidget.setHorizontalHeaderLabels(["idCar", "DateCreate", "DateClose", "idStatus", "", ""])
            if value == "ServiceList":
                self.tableWidget.setHorizontalHeaderLabels(["idOrder", "idService", "idWorker", "", "", ""])
            if value == "Service":
                self.tableWidget.setHorizontalHeaderLabels(["ServiceName", "ServiceCost", "", "", "", ""])
            if value == "Statuses":
                self.tableWidget.setHorizontalHeaderLabels(["StatusName", "", "", "", "", ""])
            if value == "TimeSheet":
                self.tableWidget.setHorizontalHeaderLabels(["idOrder", "idWorker", "WorkedHours", "", "", ""])
            if value == "Worker":
                if self.prior == "Admin":
                    self.tableWidget.setColumnCount(7)
                    self.tableWidget.setHorizontalHeaderLabels(["WorkerName", "WorkerSurname", "Phone", "Position", "Salary", "Login", "Password"])
                else:
                    mess = QtWidgets.QMessageBox()
                    mess.setText("Access denied!")
                    mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    mess.exec_()


    def warning(self, message):
        mess = QtWidgets.QMessageBox()
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec_()

    def UPDATE(self):
        cursor = cnxn.cursor()
        value = self.id_line.text()
        table = self.Tables_combobox.currentText()
        rowCount = self.tableWidget.rowCount()
        if value == '':
            self.warning("Enter required ID")
        else:
            if table == "Orders":
                for row in range(rowCount):
                    if value == self.tableWidget.item(row, 0).text():
                        data = []
                        for column in range(5):
                            test = self.tableWidget.item(row, column).text()
                            data.append("'" + test + "'")
                        command = "update Orders set idCar = " + data[1] + ", DateCreate = " + data[2] + ", DateClose = " + data[3] + ", idStatus = " + data[4] + " where idOrder = " + value
                        cursor.execute(command)
                        cnxn.commit()
                        self.COMBOBOX()
            if table == "Client":
                for row in range(rowCount):
                    if value == self.tableWidget.item(row, 0).text():
                        data = []
                        for column in range(5):
                            test = self.tableWidget.item(row, column).text()
                            data.append("'" + test + "'")
                        command = "update Client set ClientName = " + data[1] + ", ClientSurname = " + data[2] + ", BirthDate = " + data[3] + ", Phone = " + data[4] + " where idClient = " + value
                        cursor.execute(command)
                        cnxn.commit()
                        self.COMBOBOX()
            if table == "Car":
                for row in range(rowCount):
                    if value == self.tableWidget.item(row, 0).text():
                        data = []
                        for column in range(4):
                            test = self.tableWidget.item(row, column).text()
                            data.append("'" + test + "'")
                        command = "update Car set idClient = " + data[1] + ", Model = " + data[2] + ", Plate = " + data[3] + " where idCar = " + value
                        cursor.execute(command)
                        cnxn.commit()
                        self.COMBOBOX()
            if table == "Worker":
                if self.prior == "Admin":
                    for row in range(rowCount):
                        if value == self.tableWidget.item(row, 0).text():
                            data = []
                            for column in range(8):
                                test = self.tableWidget.item(row, column).text()
                                data.append(test)
                            pwd = cipher.encrypt(data[7].encode('utf-8')).decode('utf-8')
                            command = "update Worker set WorkerName = '" + data[1] + "', WorkerSurname = '" + data[2] + "', Phone = '" + data[3] + "', Position = '" + data[4] + "', Salary = " + data[5] + ", WorkerLogin = '" + data[6] + "', WorkerPassword = '" + pwd + "' where idWorker = " + value
                            print(command)
                            cursor.execute(command)
                            cnxn.commit()
                            self.COMBOBOX()
                else:
                    mess = QtWidgets.QMessageBox()
                    mess.setText("Access denied!")
                    mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    mess.exec_()
            if table == "Details":
                for row in range(rowCount):
                    if value == self.tableWidget.item(row, 0).text():
                        data = []
                        for column in range(4):
                            test = self.tableWidget.item(row, column).text()
                            data.append("'" + test + "'")
                        command = "update Details set DetailName = " + data[1] + ", DetailCost = " + data[2] + ", DetailCount = " + data[3] + " where idDetail = " + value
                        cursor.execute(command)
                        cnxn.commit()
                        self.COMBOBOX()
            if table == "Service":
                for row in range(rowCount):
                    if value == self.tableWidget.item(row, 0).text():
                        data = []
                        for column in range(3):
                            test = self.tableWidget.item(row, column).text()
                            data.append("'" + test + "'")
                        command = "update Servise set ServiceName = " + data[1] + ", ServiceCost = " + data[2] + " where idService = " + value
                        cursor.execute(command)
                        cnxn.commit()
                        self.COMBOBOX()
            if table == "DetailsRequest":
                for row in range(rowCount):
                    if value == self.tableWidget.item(row, 0).text():
                        data = []
                        for column in range(3):
                            test = self.tableWidget.item(row, column).text()
                            data.append(test)
                        command = "update DetailsRequest set idStatus = " + data[1] + ", idServiceList = " + data[2] + " where idRequest = " + value
                        cursor.execute(command)
                        cnxn.commit()
                        self.COMBOBOX()
            if table == "Statuses":
                for row in range(rowCount):
                    if value == self.tableWidget.item(row, 0).text():
                        data = []
                        for column in range(2):
                            test = self.tableWidget.item(row, column).text()
                            data.append("'" + test + "'")
                        command = "update Statuses set StatusName = " + data[1] + " where idStatus = " + value
                        cursor.execute(command)
                        cnxn.commit()
                        self.COMBOBOX()
            if table == "DetailsList":
                for row in range(rowCount):
                    if value == self.tableWidget.item(row, 0).text():
                        data = []
                        for column in range(4):
                            test = self.tableWidget.item(row, column).text()
                            data.append(test)
                        command = "update DetailsList set idDetail = " + data[1] + ", DetailCount = " + data[2] + ", idRequest = " + data[3] + " where idDetailsList = " + value
                        cursor.execute(command)
                        cnxn.commit()
                        self.COMBOBOX()

    def DELETE(self):
        cursor = cnxn.cursor()
        value = self.id_line.text()
        table = self.Tables_combobox.currentText()
        if value == '':
            self.warning("Enter required ID")
        else:
            if table == "Orders":
                command = "delete from Orders where idOrder = " + value
                cursor.execute(command)
                cnxn.commit()
                self.COMBOBOX()
            if table == "Client":
                command = "delete from Client where idClient = " + value
                cursor.execute(command)
                cnxn.commit()
                self.COMBOBOX()
            if table == "Car":
                command = "delete from Car where idCar = " + value
                cursor.execute(command)
                cnxn.commit()
                self.COMBOBOX()
            if table == "Worker":
                if self.prior == "Admin":
                    command = "delete from Worker where idWorker = " + value
                    cursor.execute(command)
                    cnxn.commit()
                    self.COMBOBOX()
                else:
                    mess = QtWidgets.QMessageBox()
                    mess.setText("Access denied!")
                    mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    mess.exec_()
            if table == "Details":
                command = "delete from Details where idDetail = " + value
                cursor.execute(command)
                cnxn.commit()
                self.COMBOBOX()
            if table == "Service":
                command = "delete from Servise where idService = " + value
                cursor.execute(command)
                cnxn.commit()
                self.COMBOBOX()
            if table == "DetailsRequest":
                command = "delete from DetailsRequest where idRequest = " + value
                cursor.execute(command)
                cnxn.commit()
                self.COMBOBOX()
            if table == "Statuses":
                command = "delete from Statuses where idStatus = " + value
                cursor.execute(command)
                cnxn.commit()
                self.COMBOBOX()
            if table == "DetailsList":
                command = "delete from DetailsList where idDetailsList = " + value
                cursor.execute(command)
                cnxn.commit()
                self.COMBOBOX()

    def QUERIES(self):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        cursor = cnxn.cursor()
        value = self.Queries_combobox.currentText()
        if value == "Вывести детали с сортировкой по востребованности":
            command = """select Details.idDetail,Details.DetailName , sum(DetailsList.DetailCount) as 'sum'
                        from DetailsRequest
                        join DetailsList on DetailsList.idRequest = DetailsRequest.idRequest
                        join Details on Details.idDetail = DetailsList.idDetail
                        group by Details.idDetail, Details.DetailName
                        order by sum(DetailsList.idRequest) desc
            """
            self.tableWidget.setHorizontalHeaderLabels(["idDetail", "DetailName", "", "", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "Вывести самую популярную услугу":
            command = """select top 1 Servise.ServiceName, count(ServiceList.idOrder) as 'count'
                        from Servise
                        join ServiceList on ServiceList.idService = Servise.idService
                        join Orders on Orders.idOrder = ServiceList.idOrder
                        group by Servise.ServiceName
                        order by sum(ServiceList.idOrder) desc"""
            self.tableWidget.setHorizontalHeaderLabels(["idOrder", "", "", "", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "Вывести заказ-наряд со стоимостью работ для клиента":
            tempId = self.id_line.text()
            if tempId == '':
                tempId = 1
            command = """select ServiceList.idOrder, sum(Servise.ServiceCost) as 'sum'
                        from Servise
                        join ServiceList on Servise.idService = ServiceList.idService
                        join Orders on Orders.idOrder = ServiceList.idOrder
                        where Orders.idOrder = """ + str(tempId) + """
                        group by ServiceList.idOrder"""
            self.tableWidget.setHorizontalHeaderLabels(["idOrder", "Sum", "", "", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "Вывести сумму стоимостей всех работ за определенный период":
            tempDate = "'" + self.dateEdit.date().toString(QtCore.Qt.ISODate) + "'"
            currDate = "'" + self.dateEdit_2.date().toString(QtCore.Qt.ISODate) + "'"
            command = """select sum(Servise.ServiceCost) as 'sum'
                        from Orders
                        join ServiceList on ServiceList.idOrder = Orders.idOrder
                        join Servise on ServiceList.idService = Servise.idService
                        where Orders.DateCreate between """ + tempDate + " and " + currDate + """ 
                        order by sum(Servise.ServiceCost)"""
            self.tableWidget.setHorizontalHeaderLabels(["ServiceCost", "", "", "", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "Вывести все заказ-наряды для одного заказчика со стоимостью за определенный период":
            tempId = self.id_line.text()
            if tempId == '':
                tempId = 1
            tempDate = "'" + self.dateEdit.date().toString(QtCore.Qt.ISODate) + "'"
            currDate = "'" + self.dateEdit_2.date().toString(QtCore.Qt.ISODate) + "'"
            command = """select ServiceList.idOrder, sum(Servise.ServiceCost) as 'sum'
                        from Servise
                        join ServiceList on Servise.idService = ServiceList.idService
                        join Orders on Orders.idOrder = ServiceList.idOrder
                        join Car on Car.idCar = Orders.idCar
                        join Client on Client.idClient = Car.idClient
                        where Client.idClient = """ + str(tempId) + " and Orders.DateCreate between " + tempDate + " and " + currDate + """
                        group by ServiceList.idOrder"""
            self.tableWidget.setHorizontalHeaderLabels(["idOrder", "Sum", "", "", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "Вывести заказ-наряды на определенный автомобиль за период":
            tempId = self.id_line.text()
            if tempId == '':
                tempId = 1
            tempDate = "'" + self.dateEdit.date().toString(QtCore.Qt.ISODate) + "'"
            currDate = "'" + self.dateEdit_2.date().toString(QtCore.Qt.ISODate) + "'"
            command = """select Orders.idOrder
                        from Orders
                        join Car on Orders.idCar = Car.idCar
                        where Orders.idCar = """ + str(tempId) + " and Orders.DateCreate between " + tempDate + " and " + currDate + """
                        group by Orders.idOrder"""
            self.tableWidget.setHorizontalHeaderLabels(["idOrder", "", "", "", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "Вывести клиентов с несколькими автомобилями":
            command = """select  Client.idClient, Client.ClientName
                        from Client
                        join Car on Car.idClient = Client.idClient
                        group by Client.idClient, Client.ClientName having count(Client.idClient) > 1"""
            self.tableWidget.setHorizontalHeaderLabels(["idClient", "ClientName", "", "", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "Вывести количество заявок на детали за определенный период":
            tempDate = "'" + self.dateEdit.date().toString(QtCore.Qt.ISODate) + "'"
            currDate = "'" + self.dateEdit_2.date().toString(QtCore.Qt.ISODate) + "'"
            command = """select count(DetailsRequest.idRequest) as 'count'
                        from Orders
                        join ServiceList on ServiceList.idOrder = Orders.idOrder
                        join DetailsRequest on ServiceList.idServiceList = DetailsRequest.idServiceList
                        where Orders.DateCreate between """ + tempDate + " and " + currDate + """
                        order by count(DetailsRequest.idRequest)
                        """
            self.tableWidget.setHorizontalHeaderLabels(["idClient", "Count", "", "", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "Вывести заявки на детали с сортировкой по статусам":
            command = """select DetailsRequest.idRequest, DetailsRequest.idStatus
                        from DetailsRequest
                        join Statuses on DetailsRequest.idStatus = Statuses.idStatus
                        group by DetailsRequest.idRequest, DetailsRequest.idStatus
                        order by DetailsRequest.idStatus"""
            self.tableWidget.setHorizontalHeaderLabels(["idRequest", "idStatus", "", "", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "Вывести самые продолжительные по времени выполненные заказ-наряды":
            command = """select Orders.idOrder, DATEDIFF(day, Orders.DateCreate, Orders.DateClose) as "duration"
                        from Orders
                        join Statuses on Statuses.idStatus = Orders.idStatus
                        where Statuses.idStatus = 2
                        group by DATEDIFF(day, Orders.DateCreate, Orders.DateClose), Orders.idOrder"""
            self.tableWidget.setHorizontalHeaderLabels(["idOrder", "Duration", "", "", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def COMBOBOX(self):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        cursor = cnxn.cursor()
        value = self.Tables_combobox.currentText()
        if value == "Car":
            command = "select * from Car"
            self.tableWidget.setHorizontalHeaderLabels(["idCar", "idClient", "Model", "Plate", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "Client":
            command = "select * from Client"
            self.tableWidget.setHorizontalHeaderLabels(
                ["idClient", "ClientName", "ClientSurname", "BirthDate", "Phone", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "Details":
            command = "select * from Details"
            self.tableWidget.setHorizontalHeaderLabels(
                ["idDetail", "DetailName", "DetailCost", "DetailCount", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "DetailsList":
            command = "select * from DetailsList"
            self.tableWidget.setHorizontalHeaderLabels(
                ["idDetailsList", "idDetail", "DetailCount", "idRequest", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "DetailsRequest":
            command = "select * from DetailsRequest"
            self.tableWidget.setHorizontalHeaderLabels(
                ["idRequest", "idStatus", "idServiceList", "", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "Orders":
            command = "select * from Orders"
            self.tableWidget.setHorizontalHeaderLabels(
                ["idOrder", "idCar", "DateCreate", "DateClose", "idStatus", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "ServiceList":
            command = "select * from ServiceList"
            self.tableWidget.setHorizontalHeaderLabels(
                ["idServiceList", "idOrder", "idService", "idWorker", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "Service":
            command = "select * from Servise"
            self.tableWidget.setHorizontalHeaderLabels(
                ["idService", "ServiceName", "ServiceCost", "", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "Statuses":
            command = "select * from Statuses"
            self.tableWidget.setHorizontalHeaderLabels(
                ["idStatus", "StatusName", "", "", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "TimeSheet":
            command = "select * from TimeSheet"
            self.tableWidget.setHorizontalHeaderLabels(
                ["idTimeSheet", "idOrder", "idWorker", "WorkedHours", "", ""])
            result = cursor.execute(command)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if value == "Worker":
            if self.prior == "Admin":
                command = "select * from Worker"
                self.tableWidget.setColumnCount(8)
                self.tableWidget.setHorizontalHeaderLabels(
                    ["idWorker", "WorkerName", "WorkerSurname", "Phone", "Position", "Salary", "Login", "Password"])
                result = cursor.execute(command)
                for row_number, row_data in enumerate(result):
                    self.tableWidget.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            else:
                command = "select * from Worker"
                self.tableWidget.setColumnCount(6)
                self.tableWidget.setHorizontalHeaderLabels(
                    ["idWorker", "WorkerName", "WorkerSurname", "Phone", "Position", "Salary"])
                result = cursor.execute(command)
                for row_number, row_data in enumerate(result):
                    self.tableWidget.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))


def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
