from PyQt5.QtWidgets import * # noqa
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5 import QtGui
from Database import fetchLocations,fetchSitedata,editExisting
import sys
from datetime import datetime

class EditDialog(QDialog):

    def __init__(self, rowdata, locations, entryid, siteids):
        super(EditDialog, self).__init__()
        self.setWindowTitle("Editing an entry...")
        self.setFixedSize(600,100)
        self.rowdata = rowdata
        if locations[0] == 'All':
            locations.pop(0)
        self.locations = locations
        self.entryid = entryid
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
        self.dateEdit.setDate(datetime.strptime(self.rowdata[0], '%Y-%m-%d'))

        self.siteDropDown = QComboBox()
        self.siteDropDown.addItems(self.locations)
        self.siteDropDown.setCurrentIndex(self.locations.index(self.rowdata[1]))  # set it to be current site id index

        self.glassEdit = QSpinBox()
        self.paperEdit = QSpinBox()
        self.plasticEdit = QSpinBox()
        boxes = [self.glassEdit,self.paperEdit,self.plasticEdit]

        self.editGroup = QHBoxLayout()
        self.editGroup.addWidget(self.dateEdit)
        self.editGroup.addWidget(self.siteDropDown)
       
        for i in range(len(boxes)):
            boxes[i].setValue(int(self.rowdata[i + 2]))
            boxes[i].setMaximum(100)  # cant have more than 100%
            self.editGroup.addWidget(boxes[i])
    
    def oncancel(self):
        self.reject()
   
    def saveToDatabase(self):
        self.selectedlocation = self.siteids[self.siteDropDown.currentIndex()]  # we didnt need to get the siteids could have just used index
        dateboxvalue = self.dateEdit.date()
        #print(dateboxvalue)
        self.date = dateboxvalue.toPyDate()
        editExisting("Localhost",self.date,self.selectedlocation,self.glassEdit.value(), self.paperEdit.value(), self.plasticEdit.value(), self.entryid)
        self.accept()
            
#fix the resizing so that a person cant resize the editing window, but it still autoexpands to the right size
#stop 'enter' from closing the dialog
#get rid of self.siteids as it is unnecessary
#make it detect when the data hasnt been changed to avoid unnecessarily fetching and refreshing the database
