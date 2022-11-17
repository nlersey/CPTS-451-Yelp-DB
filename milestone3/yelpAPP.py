import sys
from unittest import result
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "appui.ui" 

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.Zipcodelist)
        self.ui.Zipcodelist.itemSelectionChanged.connect(self.ZipcodelistChanged)
        self.ui.Zipcodelist.itemSelectionChanged.connect(self.zipstatsNumofbus)
        self.ui.Zipcodelist.itemSelectionChanged.connect(self.zipstatsTotalpop)
        self.ui.Zipcodelist.itemSelectionChanged.connect(self.zipstatsAvgincome)
        self.ui.Zipcodelist.itemSelectionChanged.connect(self.Categories)
        self.ui.categorylist.itemSelectionChanged.connect(self.categoryChanged)
        self.ui.Zipcodelist.itemSelectionChanged.connect(self.topCategories)
        self.ui.Zipcodelist.itemSelectionChanged.connect(self.popularBusiness)
        self.ui.Zipcodelist.itemSelectionChanged.connect(self.sucessfulbusiness)

    def executeQuery(self, sql_str):
        try:
            #TODO: remember to delete password
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='cyber626'")
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
        self.ui.stateList.clear()
        sql_str= 'SELECT distinct bstate FROM business ORDER BY bstate;'
        try:
            results=self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query failed in StateList")
        self.ui.stateList.setCurrentIndex(-1) 
        self.ui.stateList.clearEditText()

    def stateChanged(self):
        self.ui.cityList.clear()
        state = self.ui.stateList.currentText()
        if (self.ui.stateList.currentIndex() >= 0 ):
            self.ui.cityList.clear()
            self.ui.businessTable.clear()
            sql_str= "SELECT distinct city FROM business WHERE bstate ='" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query failed in statechanged")
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            sql_str = "SELECT bname, baddress, city, stars, numcheckin, review_count FROM business WHERE bstate= '" + state + "'ORDER by bname;"
            try:
                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name','Address' ,'City', 'Stars','Checkins','Reviews'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 250)
                self.ui.businessTable.setColumnWidth(1, 250)
                self.ui.businessTable.setColumnWidth(2, 150)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))

                    currentRowCount += 1
            except:
                print("Query failed in StateChanged")

    def cityChanged(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            self.ui.businessTable.clear()
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems() [0].text()
            sql_str = "SELECT bname, baddress, city, stars, numcheckin, review_count FROM business WHERE bstate= '" + state + "' AND city = '" + city + "'ORDER by bname;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name','Address' ,'City', 'Stars','Checkins','Reviews'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 250)
                self.ui.businessTable.setColumnWidth(1, 250)
                self.ui.businessTable.setColumnWidth(2, 150)
                currentRowCount = 0
                for row in results:
                    self.ui.businessTable.setItem(currentRowCount, 0, QTableWidgetItem(row[0]))
                    self.ui.businessTable.setItem(currentRowCount, 1, QTableWidgetItem(row[1]))
                    self.ui.businessTable.setItem(currentRowCount, 2, QTableWidgetItem(row[2]))
                    self.ui.businessTable.setItem(currentRowCount, 3, QTableWidgetItem(str(row[3])))
                    self.ui.businessTable.setItem(currentRowCount, 4, QTableWidgetItem(str(row[4])))
                    self.ui.businessTable.setItem(currentRowCount, 5, QTableWidgetItem(str(row[5])))
                    currentRowCount += 1

            except:
                print("Query failed in citychanged")

    def Zipcodelist(self):
        self.ui.Zipcodelist.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems() [0].text()
            sql_str = "SELECT distinct zipcode FROM business WHERE bstate= '" + state + "' AND city = '" + city + "'ORDER by zipcode;"
            try:
                results = self.executeQuery(sql_str)
                #print(results)
                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.Zipcodelist.horizontalHeader().setStyleSheet(style)
                self.ui.Zipcodelist.setColumnCount(len(results[0]))
                self.ui.Zipcodelist.setRowCount(len(results))
                self.ui.Zipcodelist.setHorizontalHeaderLabels([''])
                self.ui.Zipcodelist.resizeColumnsToContents()
                currentRowCount = 0 

                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.Zipcodelist.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query failed in Zipcodelist")

    def ZipcodelistChanged(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (
                len(self.ui.Zipcodelist.selectedItems()) > 0):
            self.ui.businessTable.clear()
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.Zipcodelist.selectedItems()[0].text()
            sql_str = "SELECT bname, baddress, city, stars, numcheckin, review_count FROM business WHERE bstate = '" + state + "' AND city ='" + city + "' AND \
            zipcode ='" + zipcode + "'  "
            try:
                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name','Address' ,'City', 'Stars','Checkins','Reviews'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 250)
                self.ui.businessTable.setColumnWidth(1, 250)
                self.ui.businessTable.setColumnWidth(2, 150)
                currentRowCount = 0
                for row in results:
                    results = self.executeQuery(sql_str)
                    self.ui.businessTable.setItem(currentRowCount, 0, QTableWidgetItem(row[0]))
                    self.ui.businessTable.setItem(currentRowCount, 1, QTableWidgetItem(row[1]))
                    self.ui.businessTable.setItem(currentRowCount, 2, QTableWidgetItem(row[2]))
                    self.ui.businessTable.setItem(currentRowCount, 3, QTableWidgetItem(str(row[3])))
                    self.ui.businessTable.setItem(currentRowCount, 4, QTableWidgetItem(str(row[4])))
                    self.ui.businessTable.setItem(currentRowCount, 5, QTableWidgetItem(str(row[5])))
                    currentRowCount += 1
            except:
                print("Query failed in ZipcodelistChanged")

    def zipstatsNumofbus(self):
        self.ui.numofbusinesses.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (
                len(self.ui.Zipcodelist.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.Zipcodelist.selectedItems()[0].text()
            sql_str = "SELECT COUNT(*) AS num_bus FROM (SELECT COUNT(business_id), business_id\
	        FROM business WHERE bstate = '" + state + "' AND city ='" + city + "' AND zipcode ='" + zipcode \
                      + "' GROUP BY(business_id)) AS derivedTable "
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.numofbusinesses.addItem(str(row[0]))

    def zipstatsTotalpop(self):
        self.ui.totalpopulation.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (
                len(self.ui.Zipcodelist.selectedItems()) > 0):
            zipcode = self.ui.Zipcodelist.selectedItems()[0].text()
            sql_str = "SELECT population FROM zipcodedata WHERE zipcode ='" + zipcode + "'"
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.totalpopulation.addItem(str(row[0]))

    def zipstatsAvgincome(self):
        self.ui.avgincome.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (
                len(self.ui.Zipcodelist.selectedItems()) > 0):
            zipcode = self.ui.Zipcodelist.selectedItems()[0].text()
            sql_str = "SELECT meanIncome FROM zipcodedata WHERE zipcode ='" + zipcode + "'"
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.avgincome.addItem(str(row[0]))

    def Categories(self):
        self.ui.categorylist.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (
                len(self.ui.Zipcodelist.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.Zipcodelist.selectedItems()[0].text()
            sql_str = "SELECT DISTINCT cname FROM business, categories WHERE bstate = '" + state + "' AND city ='" + city + "' AND zipcode ='" + zipcode \
                      + "' AND business.business_id = categories.business_id ORDER BY cname "
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.categorylist.addItem(row[0])
            try:
                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.categorylist.horizontalHeader().setStyleSheet(style)
                self.ui.categorylist.setColumnCount(len(results[0]))
                self.ui.categorylist.setRowCount(len(results))
                self.ui.categorylist.setHorizontalHeaderLabels(['Categories'])
                self.ui.categorylist.resizeColumnsToContents()

                for row in results:
                    self.ui.categorylist.addItem(row[0])
            except:
                print("Query failed in Categories ")

    def categoryChanged(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (
                len(self.ui.Zipcodelist.selectedItems()) > 0) and (
                len(self.ui.categorylist.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.Zipcodelist.selectedItems()[0].text()
            category = self.ui.categorylist.selectedItems()[0].text()

            sql_str = "SELECT bname, baddress, city, stars, numcheckin, review_count FROM business, categories WHERE bstate = '" + state + "' AND city ='" + city + "' AND zipcode ='" + zipcode \
                      + "' AND cname = '" + category + "'  AND business.business_id = categories.business_id ORDER BY bname; "

            results = self.executeQuery(sql_str)
            try:
                results = self.executeQuery(sql_str)
                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name','Address' ,'City', 'Stars','Checkins','Reviews'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 250)
                self.ui.businessTable.setColumnWidth(1, 250)
                self.ui.businessTable.setColumnWidth(2, 150)

                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query failed in categoryChanged ")
        
    def topCategories(self):
        self.ui.topCategories.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (
                len(self.ui.Zipcodelist.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.Zipcodelist.selectedItems()[0].text()
            sql_str = "SELECT cname, COUNT(cname) AS num_categories FROM business, categories WHERE " \
                      "bstate = '" + state + "' AND city ='" + city + "' AND zipcode ='" + zipcode \
                      + "' AND business.business_id = categories.business_id GROUP BY cname ORDER" \
                        " BY COUNT(cname) DESC; "
            results = self.executeQuery(sql_str)
            try:
                results = self.executeQuery(sql_str)
                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.topCategories.horizontalHeader().setStyleSheet(style)
                self.ui.topCategories.setColumnCount(len(results[0]))
                self.ui.topCategories.setRowCount(len(results))
                self.ui.topCategories.setHorizontalHeaderLabels(['#of Business', 'Category'])
                self.ui.topCategories.resizeColumnsToContents()
                currentRowCount = 0
                for row in results:
                    self.ui.topCategories.setItem(currentRowCount, 0, QTableWidgetItem(str(row[1])))
                    self.ui.topCategories.setItem(currentRowCount, 1, QTableWidgetItem(row[0]))
                    currentRowCount += 1
            except:
                print("Query failed")

    def popularBusiness(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (
                len(self.ui.Zipcodelist.selectedItems()) > 0):
            zipcode = self.ui.Zipcodelist.selectedItems()[0].text()
            
            sql_str = "SELECT business.bname, checkins.total FROM business, checkins WHERE business.business_id = checkins.business_id AND zipcode = '" + zipcode + "' ORDER BY checkins.total DESC;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {"" background-color: #f3f3f3; }"
                self.ui.popBusinesses.horizontalHeader().setStyleSheet(style)
                self.ui.popBusinesses.setColumnCount(len(results[0]))
                self.ui.popBusinesses.setRowCount(len(results))
                self.ui.popBusinesses.setHorizontalHeaderLabels(
                    ['Business Name', 'recent number of checkins'])
                self.ui.popBusinesses.setColumnWidth(0, 250)
                self.ui.popBusinesses.setColumnWidth(1, 250)
                self.ui.popBusinesses.setColumnWidth(2, 150)
                currentRowCount = 0
                for row in results:
                    self.ui.popBusinesses.setItem(currentRowCount, 0, QTableWidgetItem(str(row[0])))
                    self.ui.popBusinesses.setItem(currentRowCount, 1, QTableWidgetItem(str(row[1])))

                    currentRowCount += 1
            except:
                print("Query failed popular business")

    def sucessfulbusiness(self):
            if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (
                    len(self.ui.Zipcodelist.selectedItems()) > 0):
                zipcode = self.ui.Zipcodelist.selectedItems()[0].text()
                sql_str = "SELECT business.bname, ROUND(AVG(review.stars),2) FROM business, review WHERE business.business_id = review.business_id AND zipcode = '" + zipcode + "' GROUP BY business.bname ORDER BY AVG(review.stars) DESC;"                
                try:
                    results = self.executeQuery(sql_str)
                    style = "::section {"" background-color: #f3f3f3; }"
                    self.ui.successfulbusiness.horizontalHeader().setStyleSheet(style)
                    self.ui.successfulbusiness.setColumnCount(len(results[0]))
                    self.ui.successfulbusiness.setRowCount(len(results))
                    self.ui.successfulbusiness.setHorizontalHeaderLabels(
                        ['Business Name', 'avg rating'])
                    self.ui.successfulbusiness.setColumnWidth(0, 250)
                    self.ui.successfulbusiness.setColumnWidth(1, 250)
                    self.ui.successfulbusiness.setColumnWidth(2, 150)
                    currentRowCount = 0
                    for row in results:
                        self.ui.successfulbusiness.setItem(currentRowCount, 0, QTableWidgetItem(str(row[0])))
                        self.ui.successfulbusiness.setItem(currentRowCount, 1, QTableWidgetItem(str(row[1])))

                        currentRowCount += 1
                except:
                    print("Query failed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
