import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
import sqlite3


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui", self)
        self.btn_login.clicked.connect(self.gotologin)

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btn_login.clicked.connect(self.loginfunction)

    def loginfunction(self):
        user = self.userfield.text()
        pasword = self.passwordfield.text()

        if len(user)==0 or len(pasword)==0:
            self.error.setText("Please input all fields.")

        else:
            conn = sqlite3.connect("authorization.db")
            cur = conn.cursor()
            query = "SELECT password FROM authorized WHERE username=\'"+user+"\'"
            # query = "SELECT password FROM login WHERE login=\'"+user+"\'"
            # query = f"SELECT password FROM login WHERE login='{user}'"
            cur.execute(query)
            result_pass = cur.fetchone()[0]

            if result_pass == pasword:
                print("Sucesssfully logged in")
                self.error.setText("")
            else:
                self.error.setText("Invalid usename or password")



#main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
