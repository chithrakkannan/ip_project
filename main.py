import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication, QStackedWidget
from PyQt5.QtCore import Qt

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

    """
    Table : mcq
    Field          | Type         | Null | Key | Default | Extra          |
    +----------------+--------------+------+-----+---------+----------------+
    | question_id    | int          | NO   | PRI | NULL    | auto_increment |
    | question_text  | varchar(255) | NO   |     | NULL    |                |
    | option_a       | varchar(100) | NO   |     | NULL    |                |
    | option_b       | varchar(100) | NO   |     | NULL    |                |
    | option_c       | varchar(100) | NO   |     | NULL    |                |
    | option_d       | varchar(100) | NO   |     | NULL    |                |
    | correct_option | char(1)      | NO   |     | NULL    |                |
    | category       | varchar(50)  | YES  |     | NULL    |                |
    """
# Dashboard
class Dashboard(QDialog):
    def __init__(self):
        super(Dashboard, self).__init__()
        loadUi("dashboard.ui", self)
        self.l_user.setText("")  # Assuming l_user is a label widget
        self.btn_quit.clicked.connect(self.GoToLogin)
        self.btn_quiz.clicked.connect(self.StartQuiz)
        self.btn_help.clicked.connect(self.ViewUsername)

    def GoToLogin(self):
        print("Successfully logged out")

        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def StartQuiz(self):
        print("Starting Quiz")

        quiz = Quiz(quiz_data)
        widget.addWidget(quiz)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def ViewUsername(self):
        if self.l_user.text() == "Just Start the quiz":
            self.l_user.setText("")
        else:
            self.l_user.setText("Just Start the quiz")

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
        with DatabaseManager() as db:
            username = self.txt_uname.text()
            password = self.txt_pass.text()
            # the username already exists?
            query = "SELECT username FROM users WHERE username = %s"
            db.cursor.execute(query, (username,))
            existing_username = db.cursor.fetchone()

            if existing_username:
                print("Username exists")
                query = "SELECT password FROM users WHERE username = %s"
                db.cursor.execute(query, (username,))
                stored_password = db.cursor.fetchone()

                if stored_password and password == stored_password[0]:
                    home = Dashboard()
                    widget.addWidget(home)
                    widget.setCurrentIndex(widget.currentIndex() + 1)


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
            # the username already exists?
            query = "SELECT username FROM users WHERE username = %s"
            db.cursor.execute(query, (username,))
            existing_username = db.cursor.fetchone()

            if existing_username:
                print("Username already taken")
            elif password != password_confirmation:
                print("Passwords didn't match")
            else:
                print("User registration successful")
                print("Username:", username)
                print("Password:", "*" * len(password))
                insert_query = "INSERT INTO users (first_name, last_name, username, password) VALUES (%s, %s, %s, %s)"
                db.cursor.execute(insert_query, (first_name, last_name, username, password))
                db.connection.commit()
                self.show_msg()
                self.GoToLogin()



    def show_msg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        # setting message for Message Box
        msg.setText("Registration successful, Login to continue")

        # setting Message box window title
        msg.setWindowTitle("Success")

        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok)

        # start the app
        retval = msg.exec_()


    def GoToLogin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Quiz(QDialog):
    def __init__(self, quiz_data):
        super(Quiz, self).__init__()

        self.quiz_data = quiz_data
        self.current_question = 0
        self.score = 0

        loadUi("quiz.ui", self)

        self.btn_01.clicked.connect(lambda: self.check_answer(0))
        self.btn_02.clicked.connect(lambda: self.check_answer(1))
        self.btn_03.clicked.connect(lambda: self.check_answer(2))
        self.btn_04.clicked.connect(lambda: self.check_answer(3))

        self.show_question()

    def show_question(self):
        if self.current_question < len(self.quiz_data):
            question_data = self.quiz_data[self.current_question]

            self.l_question.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.l_question.setText(question_data['question'])

            options = question_data['options']
            self.btn_01.setText(options[0])
            self.btn_02.setText(options[1])
            self.btn_03.setText(options[2])
            self.btn_04.setText(options[3])
        else:
            self.show_result()

    def check_answer(self, selected_option):
        correct_answer = self.quiz_data[self.current_question]['answer']
        if selected_option == correct_answer:
            self.score += 1
        self.current_question += 1
        self.show_question()

    def show_result(self):
        print("Scores:", self.score)
        self.show_msg()
        print("Opening Dashboard")
        dash = Dashboard()
        widget.addWidget(dash)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def show_msg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        # setting message for Message Box
        msg.setText(f"Your score is :{self.score}")

        # setting Message box window title
        msg.setWindowTitle("Question MessageBox")

        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok)

        # start the app
        retval = msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    quiz_data = [
        {
            'question': "What is the capital of France?",
            'options': ["London", "Madrid", "Paris", "Berlin"],
            'answer': 2  # The index of the correct answer (0-based)
        },
        {
            'question': "Which language is this quiz written in?",
            'options': ["Python", "Java", "C++", "JavaScript"],
            'answer': 0
        },
        {
            'question': "What is 2 + 2?",
            'options': ["3", "4", "5", "6"],
            'answer': 1
        }
        # Add more questions here
    ]

    home = Login()
    widget = QStackedWidget()
    widget.addWidget(home)
    widget.setFixedHeight(700)
    widget.setFixedWidth(1200)
    widget.show()

    try:
        sys.exit(app.exec_())
    except Exception as e:
        print("An error occurred:", str(e))
