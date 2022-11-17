import sys
from unittest import result
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "milestone2App.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone1(QMainWindow):
    def __init__(self):
        super(milestone1, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)#passing statechanged value and not statechanged() function
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.bname.textChanged.connect(self.getBusinessNames)
        self.ui.businesses.itemSelectionChanged.connect(self.displayBusinessCity)


    def executeQuery(self, sql_str):
        try:
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='cyber626'")
        except:
            print('Unable to connect to the database')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str= 'SELECT distinct state  FROM business ORDER BY state;'
        try:
            results=self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query failed")
        self.ui.stateList.setCurrentIndex(-1) #-1 means nothing is selected
        self.ui.stateList.clearEditText()

    def stateChanged(self):
        self.ui.cityList.clear()
        state = self.ui.stateList.currentText()
        if (self.ui.stateList.currentIndex() >= 0 ):
            sql_str = "SELECT distinct city FROM business WHERE state ='" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query failed in statechanged")

        sql_str = "SELECT name, city, state FROM business  WHERE state = '" + state + "' ORDER BY name ;"
        try:
            results = self.executeQuery(sql_str)
            style = "::section {""background-color: #f3f3f3; }"
            self.ui.businessTable.horizontalHeader().setStyleSheet(style)
            self.ui.businessTable.setColumnCount(len(results[0]))
            self.ui.businessTable.setRowCount(len(results))
            self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State'])
            self.ui.businessTable.resizeColumnsToContents()
            self.ui.businessTable.setColumnWidth(0,300)
            self.ui.businessTable.setColumnWidth(1,100)
            self.ui.businessTable.setColumnWidth(2,50)
            currentRowCount = 0
            for row in results:
                for colCount in range (0,len(results[0])):
                    self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(row[colCount]))
                currentRowCount += 1
        except:
            print("queryfailed statechanged2")

    def cityChanged(self):
        if (self.ui.stateList.currentIndex() >= 0 ) and (len(self.ui.cityList.selectedItems())>0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems() [0].text()
            sql_str = "SELECT name, city, state FROM business  WHERE state = '" + state + "'AND city=  '" + city + "' ORDER BY name ;"
            results = self.executeQuery(sql_str)
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,300)
                self.ui.businessTable.setColumnWidth(1,100)
                self.ui.businessTable.setColumnWidth(2,50)
                currentRowCount = 0
                for row in results:
                    for colCount in range (0,len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("query failed citychanged1")

    def getBusinessNames(self):
        self.ui.businesses.clear()
        businessname = self.ui.bname.text() #capitals matter. should change so caps or not doesnt matter
        sql_str = "SELECT name FROM business WHERE name LIKE  '%" + businessname + "%' ORDER BY name;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.businesses.addItem(row[0])
        except:
            print("query failed")

    def displayBusinessCity(self):
        businessname=self.ui.businesses.selectedItems() [0].text()
        sql_str = "SELECT city FROM business WHERE name = '" + businessname + "';"
        try:
            results = self.executeQuery(sql_str)
            #print(results)
            self.ui.bcity.setText(results[0][0])
        except:
            print ("businesscity query failed")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone1()
    window.show()
    sys.exit(app.exec_())