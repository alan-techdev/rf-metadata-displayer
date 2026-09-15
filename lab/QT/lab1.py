'''
$ export PYTHONPATH=/home/alan/workspace-python/RTL-SDR/rfmetadata/src
$ pwd 
 /home/alan/workspace-python/RTL-SDR/rfmetadata/src
$ python rfmetadata ???
'''

import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QApplication, QWidget, QGroupBox, QVBoxLayout, QLabel


class MyWidget(QtWidgets.QWidget):
   def __init__(self):
        super().__init__()

        self.groupBox = QGroupBox("My Group Box Title")
        self.layout = QVBoxLayout(self)
        label1 = QLabel("Label 1")
        label2 = QLabel("Label 2")
        self.layout.addWidget(label1)
        self.layout.addWidget(label2)

        self.groupBox.setLayout(self.layout)

   def search_power(self,power,frequency):
      pass

def main()-> None:

   app = QtWidgets.QApplication()

   widget = MyWidget()
   widget.resize(800,600)
   widget.setWindowTitle("RFDisplay")
   widget.show()

   sys.exit(app.exec())

# this is important so that it does not run from pytest 
if __name__ == "__main__": 
    main()