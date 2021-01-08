from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5 import QtGui
from Database import fetchLocations,fetchSitedata
import sys
from datetime import datetime

class EditDialog(QDialog):

    def __init__(self, rowdata, locations):
        super(EditDialog, self).__init__()
        self.setWindowTitle("Editing an entry...")
        self.setFixedSize(600,100)
        self.rowdata = rowdata
        locations.pop(0)
        self.locations = locations
        self.initeditingBoxes()
        
        self.label= QLabel(str(rowdata))
        buttons = QDialogButtonBox.Save | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.editGroup)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def initeditingBoxes(self):
        dateEdit = QDateEdit()
        dateEdit.setDate(datetime.strptime(self.rowdata[0], '%Y-%m-%d'))

        self.siteDropDown = QComboBox()
        self.siteDropDown.addItems(self.locations)

        self.glassEdit = QSpinBox()
        self.paperEdit = QSpinBox()
        self.plasticEdit = QSpinBox()
        boxes = [self.glassEdit,self.paperEdit,self.plasticEdit]

        self.editGroup = QHBoxLayout()
        self.editGroup.addWidget(dateEdit)
        self.editGroup.addWidget(self.siteDropDown)
       
        for i in range(len(boxes)):
            boxes[i].setValue(int(self.rowdata[i+2]))
            boxes[i].setMaximum(100)
            self.editGroup.addWidget(boxes[i])

        
#fix the resizing so that a person cant resize the editing window, but it still autoexpands to the right size
#stop 'enter' from closing the dialog



    


