from PyQt5.QtWidgets import * # noqa
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5 import QtGui
from Database import fetchLocations,fetchSitedata,editExisting
import sys
from datetime import datetime

class ChooseDialog(QDialog):

    def __init__(self,all_locations):
        super(ChooseDialog, self).__init__()
        self.setWindowTitle("Select which sites to include...")
        self.setFixedSize(600,600)
        self.all_locations = all_locations
        self.selectedlist = []
        self.initmainblock()
        self.numsincelastbreak = 0  # counting number of sites on each line
        
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
        self.checkboxlayout = QVBoxLayout()
        self.checkboxgroup = QButtonGroup()
        self.checkboxgroup.setExclusive(False)

        for i in range(len(self.all_locations)):
            tempbox = QCheckBox(self.all_locations[i])
            self.checkboxlayout.addWidget(tempbox)
            self.checkboxgroup.addButton(tempbox)
            tempbox.stateChanged.connect(self.boxchecked2)

        self.listsites = QLabel('Selected Sites: ')
        self.listsites.setWordWrap(True)
        containerwidget.setLayout(self.checkboxlayout)
        self.scrollarea.setWidget(containerwidget)

        self.blocklayout.addWidget(self.scrollarea)
        self.blocklayout.addWidget(self.listsites)

    def boxchecked(self):  # 0 is unchecked 2 is checked state
        obj = self.sender()
        name = obj.text()
        text = self.listsites.text()
        if obj.checkState() == 2:
            self.selectedlist.append(name)
            if self.numsincelastbreak == 2:
                name = name + '\n'
                self.numsincelastbreak = 0
            else:
                self.numsincelastbreak += 1
            if len(text) > 16:
                newtext = text + ', ' + name
            else:
                newtext = text + name
            self.listsites.setText(newtext)
        else:
            self.selectedlist.pop(self.selectedlist.index(name))
            for i in range(2,len(self.selectedlist),2):
                self.selectedlist[i] = self.selectedlist[i] + '\n'
            newtext = 'Selected Sites: ' + ((str(self.selectedlist).replace('[','')).replace(']','')).replace('\'','')
            self.listsites.setText(newtext)
        print(self.selectedlist)

    def boxchecked2(self):  # 0 is unchecked 2 is checked state
        obj = self.sender()
        name = obj.text()
        text = self.listsites.text()
        if obj.checkState() == 2:
            self.selectedlist.append(name)
            if len(text) > 16:
                newtext = text + ', ' + name
            else:
                newtext = text + name
            self.listsites.setText(newtext)
        else:
            self.selectedlist.pop(self.selectedlist.index(name))
            newtext = 'Selected Sites: ' + ((str(self.selectedlist).replace('[','')).replace(']','')).replace('\'','')
            self.listsites.setText(newtext)
        
    def oncancel(self):
        self.reject()
   
    def onaccept(self):
        self.accept()

if __name__ == "__main__":
    foo = ChooseDialog('bar')
