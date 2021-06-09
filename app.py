from subprocess import run, PIPE
from multiprocessing import freeze_support

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QCoreApplication, QThread
from PySide6.QtUiTools import QUiLoader
from qt_material import apply_stylesheet, QtStyleTools

import Subdomain.parsing_yh as parsing


# Extra stylesheets
extra = {

    # Button colors
    'danger': '#dc3545',
    'warning': '#ffc107',
    'success': '#17a2b8',
    # Font
    'font_family': 'Malgun Gothic',
}


class GetParsingThread(QThread):
    def __init__(self, parent_class):
        super(GetParsingThread, self).__init__()
        self.parent = parent_class

    def run(self):
        parsing.main(self.parent.main.lineEdit.text(), False, None, None, None)


class GetSQLMapThread(QThread):
    def __init__(self, parent_class):
        super(GetSQLMapThread, self).__init__()
        self.parent = parent_class

    def run(self):
        #
        parsing.main(self.parent.main.lineEdit.text(), False, None, None, None)
        self.parent.main.plainTextEdit.appendPlainText("Parsing End.")
        #
        with open('sqlmap_list.txt', 'r', encoding='UTF-8') as textfile:
            for line in textfile:
                print("python sqlmap/sqlmap.py " + line.strip('\n') + " --timeout=2")
                output = run("python sqlmap/sqlmap.py " + line.strip('\n') + " --timeout=2",
                             stdin=PIPE, capture_output=True, text=True)
                print(output.stdout)
                # self.parent.main.plainTextEdit.appendPlainText(output.stdout)
        self.parent.main.plainTextEdit.appendPlainText("SQLMap End.")
        #
        with open('xss_list.txt', 'r', encoding='UTF-8') as textfile:
            for line in textfile:
                print("python XSStrike/xsstrike.py " + line.strip('\n'))
                output = run("python XSStrike/xsstrike.py " + line.strip('\n'),
                             stdin=PIPE, capture_output=True, text=True)
                print(output.stdout)
                # self.parent.main.plainTextEdit.appendPlainText(output.stdout)
        self.parent.main.plainTextEdit.appendPlainText("XXStrike End.")


class RuntimeStylesheets(QMainWindow, QtStyleTools):
    def __init__(self):
        """Constructor"""
        super().__init__()

        self.main = QUiLoader().load('main_window.ui', self)
        self.setWindowIcon(QIcon('icon.ico'))
        self.main.plainTextEdit.setReadOnly(True)
        print(self.main.LoginComboBox.currentText())

        # 버튼 정의
        self.main.pushButton.clicked.connect(self.start_button)

        # 스레드 정의
        self.get_sqlmap = GetSQLMapThread(self)
        self.get_parsing = GetParsingThread(self)

    def start_button(self):
        self.get_sqlmap.start()


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








