from PyQt5.QtWidgets import * # noqa
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5 import QtGui
from Database import fetchLocations,fetchSitedata,editExisting
import sys
from datetime import datetime
import os

class CompareDialog(QDialog):

    def __init__(self,ischosen, alreadyselected):
        super(CompareDialog, self).__init__()
        self.ischosen = ischosen
        self.alreadyselected = alreadyselected
        self.setWindowTitle("Select a Past Report to Compare With...")
        self.initmainblock()
        
        buttons = QDialogButtonBox.Save | QDialogButtonBox.Cancel  # change this so that it doesnt trigger when pressing enter
        self.buttonBox = QDialogButtonBox(buttons)
        self.deselectButton = QPushButton('Deselect')
        self.deselectButton.clicked.connect(self.deselectbuttonpressed)
        self.buttonBox.accepted.connect(self.onaccept)
        self.buttonBox.rejected.connect(self.oncancel)
        self.buttonline = QHBoxLayout()
        self.buttonline.addWidget(self.deselectButton)
        self.buttonline.addWidget(self.buttonBox)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.blocklayout)
        self.layout.addLayout(self.buttonline)
        self.setLayout(self.layout)

    def initmainblock(self):
        self.blocklayout = QVBoxLayout()
        self.scrollarea = QScrollArea()
        containerwidget = QWidget()
        self.radiobuttonlayout = QVBoxLayout()
        self.radiobuttongroup = QButtonGroup()

        PastReports = os.listdir('Past_Reports')
        radiobuttons = []
        for i in range(len(PastReports)):
            tempbox = QRadioButton(PastReports[i])
            tempbox.clicked.connect(self.radiobuttontoggled)
            radiobuttons.append(tempbox)
            self.radiobuttonlayout.addWidget(tempbox)
            self.radiobuttongroup.addButton(tempbox,i)
        
        if self.ischosen:
            radiobuttons[self.alreadyselected].setChecked(True)
            self.buttonChecked = radiobuttons[self.alreadyselected]
        
        containerwidget.setLayout(self.radiobuttonlayout)
        self.scrollarea.setWidget(containerwidget)
        self.blocklayout.addWidget(self.scrollarea)
    
    def radiobuttontoggled(self):
        obj = self.sender()
        self.buttonChecked = obj

    def deselectbuttonpressed(self):
        try:
            self.radiobuttongroup.setExclusive(False)
            self.buttonChecked.setChecked(False)
            self.radiobuttongroup.setExclusive(True)
        except AttributeError:
            return

    def oncancel(self):
        self.reject()
   
    def onaccept(self):
        self.accept()

if __name__ == "__main__":
    foo = CreateDialog('bar')
