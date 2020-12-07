from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget
from PyQt5.QtGui import QIcon
import sys

class TabWidget(QDialog):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NEL Wastebase")
        self.setWindowIcon(QIcon("gearicon.jpg"))

app = QApplication(sys.argv)
mainWindow = TabWidget()
mainWindow.show()
app.exec()