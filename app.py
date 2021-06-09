import os
import datetime
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


def now_time():
    return datetime.datetime.now().strftime('%H:%M:%S')


class GetSubdomainThread(QThread):
    def __init__(self, parent_class):
        super(GetSubdomainThread, self).__init__()
        self.parent = parent_class

    def run(self):
        line_text = self.parent.main.domainLineEdit.text()
        os.system(f"python Subdomain/my_subdomain.py -d {line_text} -p 80,443 -o log.csv")
        self.parent.main.domainPlainTextEdit.appendPlainText(f"[{line_text}][{now_time()}] Search End.")


class GetSQLMapThread(QThread):
    def __init__(self, parent_class):
        super(GetSQLMapThread, self).__init__()
        self.parent = parent_class

    def run(self):
        line_text = self.parent.main.webLineEdit.text()
        #
        parsing.main(line_text, False, None, None, None)
        self.parent.main.webPlainTextEdit.appendPlainText(f"[{line_text}][{now_time()}] Parsing End.")
        #
        with open('sqlmap_list.txt', 'r', encoding='UTF-8') as textfile:
            for line in textfile:
                print("python sqlmap/sqlmap.py " + line + " --timeout=2")
                os.system("python sqlmap/sqlmap.py " + line + " --timeout=2")
                # self.parent.main.logTextEdit.appendPlainText(output)
        self.parent.main.webPlainTextEdit.appendPlainText(f"[{line_text}][{now_time()}] SQLMap End.")
        #
        with open('xss_list.txt', 'r', encoding='UTF-8') as textfile:
            for line in textfile:
                print("python XSStrike/xsstrike.py " + line)
                os.system("python XSStrike/xsstrike.py " + line)
                # self.parent.main.logTextEdit.appendPlainText(output)
        self.parent.main.webPlainTextEdit.appendPlainText(f"[{line_text}][{now_time()}] XXStrike End.")


class RuntimeStylesheets(QMainWindow, QtStyleTools):
    def __init__(self):
        """Constructor"""
        super().__init__()

        self.main = QUiLoader().load('main_window.ui', self)
        self.setWindowIcon(QIcon('icon.ico'))
        self.main.webPlainTextEdit.setReadOnly(True)
        self.main.domainPlainTextEdit.setReadOnly(True)

        # 버튼 정의
        self.main.webPushButton.clicked.connect(self.web_button)
        self.main.domainPushButton.clicked.connect(self.subdomain_button)

        # 스레드 정의
        self.get_sqlmap = GetSQLMapThread(self)
        self.get_subdomain = GetSubdomainThread(self)

    def web_button(self):
        self.get_sqlmap.start()

    def subdomain_button(self):
        self.get_subdomain.start()


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








