'''
Reed midterm project
https://www.pythonguis.com/tutorials/pyqt-signals-slots-events/
'''

from PyQt5.QtWidgets import QApplication, QWidget

import sys


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('Reed midterm project')
window.resize(500, 500)
window.show()

app.exec_()
