from PyQt5.QtWidgets import * # noqa
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5 import QtGui

class AddSite(QDialog):

    def __init__(self):
        super(AddSite, self).__init__()
        self.setWindowTitle("Adding a new site...")
        self.setFixedSize(600,100)
        self.initeditingBoxes()

        buttons = QDialogButtonBox.Save | QDialogButtonBox.Cancel  # change this so that it doesnt trigger when pressing enter

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.editGroup)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def initeditingBoxes(self):  # dont allow blank, dont allow numbers
        self.nameLine = QLineEdit()
        self.addglassbins = QSpinBox()
        self.addpaperbins = QSpinBox()
        self.addplasticbins = QSpinBox()
        boxes = [self.addglassbins,self.addpaperbins,self.addplasticbins]

        self.editGroup = QHBoxLayout()
        self.editGroup.addWidget(self.nameLine)

        for i in range(len(boxes)):
            self.editGroup.addWidget(boxes[i])
            
#fix the resizing so that a person cant resize the editing window, but it still autoexpands to the right size
