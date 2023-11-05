import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
import mysql.connector

# Database Connection
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "test01"
}

class DatabaseManager:
    def __enter__(self):
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# Dashboard
class Dashboard(QDialog):
    def __init__(self):
        super(Dashboard, self).__init__()
        loadUi("dashboard.ui", self)
        self.btn_quit.clicked.connect(self.GoToDashboard)

    def GoToDashboard(self):
        print("Successfully logged out")

        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# Login Page
class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.btn_Submit.clicked.connect(self.CheckPass)
        self.btn_newacc.clicked.connect(self.gotojoin)

    def gotojoin(self):
        join = JoinUS()
        widget.addWidget(join)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def CheckPass(self):
        user = self.txt_uname.text()
        password = self.txt_pass.text()

        with DatabaseManager() as db:
            query = "SELECT username, password FROM users WHERE username = %s"
            db.cursor.execute(query, (user,))
            result = db.cursor.fetchone()

            if result:
                stored_username, stored_password = result
                if password == stored_password:
                    print("Login Success")
                    dash = Dashboard()
                    widget.addWidget(dash)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                else:
                    print("Wrong Password")
            else:
                print("User not found")

# Join Us
class JoinUS(QDialog):
    def __init__(self):
        super(JoinUS, self).__init__()
        loadUi("join.ui", self)
        self.btn_submit.clicked.connect(self.CheckUser)
        self.btn_exuser.clicked.connect(self.GoToLogin)

    def CheckUser(self):
        # Get user input
        last_name = self.txt_lname.text()
        first_name = self.txt_fname.text()
        username = self.txt_username.text()
        password = self.txt_password.text()
        password_confirmation = self.txt_passwordc.text()

        with DatabaseManager() as db:
            # Execute a query to check if the username already exists
            query = "SELECT username FROM users WHERE username = %s"
            db.cursor.execute(query, (username,))
            existing_username = db.cursor.fetchone()

            if existing_username:
                print("Username already taken")
            elif password != password_confirmation:
                print("Passwords didn't match")
            else:
                print("First Name:", first_name)
                print("Last Name:", last_name)
                print("Username:", username)
                print("Password:", "*" * len(password))

    def GoToLogin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

app = QApplication(sys.argv)
home = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(home)
widget.setFixedHeight(700)
widget.setFixedWidth(1200)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
