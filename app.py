import os
from multiprocessing import freeze_support
import time

from PySide6.QtWidgets import QApplication, QMainWindow, QStatusBar
from PySide6.QtCore import QTimer, Qt, QCoreApplication
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtUiTools import QUiLoader
from qt_material import apply_stylesheet, QtStyleTools

import Subdomain.parsing as parsing


# Extra stylesheets
extra = {

    # Button colors
    'danger': '#dc3545',
    'warning': '#ffc107',
    'success': '#17a2b8',

    # Font
    'font_family': 'Malgun Gothic',
}


########################################################################
class RuntimeStylesheets(QMainWindow, QtStyleTools):
    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super().__init__()

        self.main = QUiLoader().load('main_window.ui', self)
        self.main.pushButton.clicked.connect(self.print_button)
        self.main.plainTextEdit.setReadOnly(True)

    def print_button(self):
        parsing.main()
        self.main.plainTextEdit.appendPlainText("Parsing End.")


if __name__ == "__main__":

    freeze_support()
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    app = QApplication([])
    app.processEvents()
    app.setQuitOnLastWindowClosed(False)
    app.lastWindowClosed.connect(lambda: app.quit())

    # Set theme
    apply_stylesheet(app, theme='dark_cyan.xml', extra=extra)

    frame = RuntimeStylesheets()
    frame.main.show()

    app.exec_()








