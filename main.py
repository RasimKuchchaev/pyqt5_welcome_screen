import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
import sqlite3


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui", self)
        self.btn_login.clicked.connect(self.gotologin)
        self.btn_create.clicked.connect(self.gotocreate)


    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotocreate(self):
        create = CreateAccScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex()+1)


class CreateAccScreen(QDialog):
    def __init__(self):
        super(CreateAccScreen, self).__init__()
        loadUi("createacc.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btn_signup.clicked.connect(self.signupfunction)

    def signupfunction(self):
        user = self.userfield.text()
        password = self.passwordfield.text()
        confirmpassword = self.confirmpasswordfield.text()

        if len(user)==0 or len(password)==0 or len(confirmpassword)==0:
            self.error_2.setText('Please fill in all input.')
        elif password != confirmpassword:
            self.error_2.setText('Password do not match.')
        else:
            conn = sqlite3.connect('authorization.db')
            cur = conn.cursor()

            user_info = [user, password]
            # cur.execute('INSERT INTO authorized (username, password) VALUES (?,?)', user_info)

            cur.execute(f"INSERT INTO authorized (username, password) VALUES {user, password}")

            conn.commit()
            conn.close()

            fillprofile = FillProfileScreen()
            widget.addWidget(fillprofile)
            widget.setCurrentIndex(widget.currentIndex()+1)


class FillProfileScreen(QDialog):
    def __init__(self):
        super(FillProfileScreen, self).__init__()
        loadUi("fillprofile.ui", self)

        self.l_image.setPixmap(QPixmap('placeholder.png'))



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

