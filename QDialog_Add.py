from PyQt5.QtWidgets import * # noqa
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5 import QtGui
from Database import addTo,fetchLocations
import sys
from datetime import datetime

class AddDialog(QDialog):

    def __init__(self, locations,siteids,user,password,host):
        super(AddDialog, self).__init__()
        self.user = user
        self.password = password
        self.host = host
        self.setWindowTitle("Adding a new entry...")
        self.setFixedSize(600,100)

        self.locationInfo = fetchLocations(user,password,host)

        if locations[0] == 'All':
            locations.pop(0)
        self.locations = locations
        self.siteids = siteids
        self.initeditingBoxes()
        

        buttons = QDialogButtonBox.Save | QDialogButtonBox.Cancel  # change this so that it doesnt trigger when pressing enter

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.saveToDatabase)
        self.buttonBox.rejected.connect(self.oncancel)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.editGroup)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def initeditingBoxes(self):
        self.dateEdit = QDateEdit()
        self.dateEdit.setDate(datetime.today())

        self.siteDropDown = QComboBox()
        self.siteDropDown.addItems(self.locations)
        self.siteDropDown.currentIndexChanged.connect(self.checkIfDisable)
        
        self.glassEdit = QSpinBox()
        self.paperEdit = QSpinBox()
        self.plasticEdit = QSpinBox()
        self.boxes = [self.glassEdit,self.paperEdit,self.plasticEdit]

        self.editGroup = QHBoxLayout()
        self.editGroup.addWidget(self.dateEdit)
        self.editGroup.addWidget(self.siteDropDown)
       
        for i in range(len(self.boxes)):
            self.boxes[i].setMaximum(100)  # cant have more than 100%
            self.editGroup.addWidget(self.boxes[i])

    def checkIfDisable(self):
        x = self.siteDropDown.currentIndex()
        binnumbers = self.locationInfo[x][2:]
        print(binnumbers)
        for i in range(len(binnumbers)):
            if binnumbers[i] == 0:
                self.boxes[i].setDisabled(True)
            else:
                self.boxes[i].setDisabled(False)
    
    def oncancel(self):
        self.reject()
   
    def saveToDatabase(self):
        self.selectedlocation = self.siteids[self.siteDropDown.currentIndex()]  # we didnt need to get the siteids could have just used index + 1 i think
        dateboxvalue = self.dateEdit.date()
        self.date = dateboxvalue.toPyDate()
        addTo(self.user,self.password,self.host,self.date,self.selectedlocation,self.glassEdit.value(), self.paperEdit.value(), self.plasticEdit.value())
        self.accept()
            
#fix the resizing so that a person cant resize the editing window, but it still autoexpands to the right size
#stop 'enter' from closing the dialog
#get rid of self.siteids as it is unnecessary
#make it detect when the data hasnt been changed to avoid unnecessarily fetching and refreshing the database

#add and edit could technically be the same QDialog if i want to, make an add class which edit inherits from