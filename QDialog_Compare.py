from PyQt5.QtWidgets import * # noqa
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5 import QtGui
from Database import fetchLocations,fetchSitedata,editExisting
import sys
from datetime import datetime
import os

class CompareDialog(QDialog):

    def __init__(self):
        super(CompareDialog, self).__init__()
        self.setWindowTitle("Select a Past Report to Compare With...")
        self.setFixedSize(600,600)
        self.initmainblock()
        
        buttons = QDialogButtonBox.Save | QDialogButtonBox.Cancel  # change this so that it doesnt trigger when pressing enter
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.onaccept)
        self.buttonBox.rejected.connect(self.oncancel)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.blocklayout)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def initmainblock(self):
        self.blocklayout = QVBoxLayout()
        self.scrollarea = QScrollArea()
        containerwidget = QWidget()
        self.radiobuttonlayout = QVBoxLayout()
        self.radiobuttongroup = QButtonGroup()

        PastReports = os.listdir('Past_Reports')

        for i in range(len(PastReports)):
            tempbox = QRadioButton(self.PastReports[i])
            self.radiobuttonlayout.addWidget(tempbox)
            self.radiobuttongroup.addButton(tempbox)
        self.blocklayout.addWidget(self.scrollarea)
        self.blocklayout.addWidget(self.listsites)

    def oncancel(self):
        self.reject()
   
    def onaccept(self):
        self.accept()

if __name__ == "__main__":
    foo = CreateDialog('bar')
