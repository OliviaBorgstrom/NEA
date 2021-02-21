from PyQt5.QtWidgets import * # noqa
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5 import QtGui
from are_you_sure_about_that import AreYouSure
import re
from QDialog_AddSite import AddSite
from Database import fetchLocations
from Database import deleteLocation
from Database import addLocation
import sys

class ConfigureDialog(QDialog):

    def __init__(self,user,password,host):
        super(ConfigureDialog, self).__init__()
        self.user = user
        self.password = password
        self.host = host
        self.setFixedSize(600,400)
        self.validRowSelected = False
        self.anythingChanged = False
       
        fetchedlocations = fetchLocations(self.user,self.password,self.host)
        self.rawlocations = [(each[1],str(each[4]),str(each[3]),str(each[2])) for each in fetchedlocations]
        self.currentlocationIDs = [each[0] for each in fetchedlocations]
        
        self.setWindowTitle("Configure your sites")
        self.currentTableData = self.rawlocations
        #buttons = QDialogButtonBox.Save | QDialogButtonBox.Cancel  # change this so that it doesnt trigger when pressing enter
        self.button = QPushButton('Done')

        #self.buttonBox = QDialogButtonBox(buttons)
        self.button.clicked.connect(self.ondone)
        #self.buttonBox.rejected.connect(self.oncancel)
        self.buttonBox = QHBoxLayout()
        self.buttonBox.addWidget(self.button)
        self.buttonBox.setAlignment(QtCore.Qt.AlignRight)

        self.init_table()
        self.init_pushButton_row()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.dataTable)
        self.layout.addLayout(self.row)
        self.layout.addLayout(self.buttonBox)
        self.setLayout(self.layout)

    def init_table(self):
        self.dataTable = QTableWidget()
        self.dataTable.setColumnCount(4)
        self.dataTable.setRowCount(70)
        self.dataTable.setHorizontalHeaderLabels(["Site Name", "Glass bins", "Paper bins", "Plastic bins"])
        self.dataTable.horizontalHeader().setSectionResizeMode(1)
        self.dataTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dataTable.cellClicked.connect(self.rowclicked)
        self.appendToTable(self.rawlocations)
        self.dataTable.resizeColumnsToContents()
    
    def appendToTable(self,data):
        self.dataTable.clearContents()
        for i in range(len(data)):
            for j in range(len(data[i])):
                item = QTableWidgetItem(data[i][j])
                item.setToolTip(data[i][j])
                self.dataTable.setItem(i,j,QTableWidgetItem(data[i][j]))
        self.currentTableData = data

    def rowclicked(self,row):
        try:
            self.currentRowSelected = self.currentTableData[row]
        except IndexError:
            self.validRowSelected = False
        else:
            self.validRowSelected = True
            self.selectedlocationID = self.currentlocationIDs[row]  # it needs the selected entryID to know what change in the database # noqa
            #print("Row %d was clicked" % (row))
    
    def init_pushButton_row(self):
        self.row = QHBoxLayout()

        self.addButton = QPushButton('Add')
        self.addButton.setToolTip('Add a new site')
        self.addButton.setFixedSize(QtCore.QSize(120,30))
        self.addButton.clicked.connect(self.executeAdd)

        self.deleteButton = QPushButton('Delete')
        self.deleteButton.setToolTip('Delete a site')
        self.deleteButton.setFixedSize(QtCore.QSize(120,30))
        self.deleteButton.clicked.connect(self.executeDelete)

        self.row.addWidget(self.addButton)
        self.row.addWidget(self.deleteButton)
        self.row.addStretch(1)

    def executeAdd(self):
        addsite = AddSite()
        state = addsite.exec()
        if state == 1:
            if len(addsite.nameLine.text()) == 0:
                self.showAnError('A new site must have a name!')
            elif self.hasNumbers(addsite.nameLine.text()):
                self.showAnError('A site name should contain only letters, not numbers!')
            else:
                self.anythingChanged = True
                addLocation(self.user,self.password,self.host,
                            addsite.nameLine.text(),addsite.addglassbins.value(),
                            addsite.addpaperbins.value(),addsite.addplasticbins.value())
                self.refresh2()
        else:
            print('cancelled')

    def hasNumbers(self,inputString):
        return bool(re.search(r'\d', inputString))

    def showAnError(self,msg):
        errorwin = QMessageBox()
        errorwin.setIcon(QMessageBox.Critical)
        errorwin.setText(msg)
        errorwin.setWindowTitle("Error")
        errorwin.exec_()

    def executeDelete(self):
        if not self.validRowSelected:
            return
        else:
            areyousure = AreYouSure()
            decide = areyousure.exec()
            if decide == 1:
                print("deleted")
                self.anythingChanged = True
                deleteLocation(self.user,self.password,self.host,self.selectedlocationID)
                self.refresh2()
            else:
                return

    def refresh2(self):
        fetchedlocations = fetchLocations(self.user,self.password,self.host)
        self.rawlocations = [(each[1],str(each[4]),str(each[3]),str(each[2])) for each in fetchedlocations]
        self.currentlocationIDs = [each[0] for each in fetchedlocations]
        self.appendToTable(self.rawlocations)

    def refresh(self,func):
        def wrapper():
            func()
            fetchedlocations = fetchLocations(self.user,self.password,self.host)
            self.rawlocations = [(each[1],str(each[4]),str(each[3]),str(each[2])) for each in fetchedlocations]
            self.currentlocationIDs = [each[0] for each in fetchedlocations]
            self.appendToTable(self.rawlocations)
        return wrapper
    
    def ondone(self):
        if self.anythingChanged:
            self.accept()
        else:
            self.reject()
            
#fix the resizing so that a person cant resize the editing window, but it still autoexpands to the right size
#stop 'enter' from closing the dialog
#get rid of self.siteids as it is unnecessary
#make it detect when the data hasnt been changed to avoid unnecessarily fetching and refreshing the database
