import sys
import csv
import mysql.connector

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication, QStackedWidget
from PyQt5.QtCore import Qt, pyqtSignal

# Database Connection
db_config = {
    "host": "localhost",
    "user": "ip",
    "password": "1234",
    "database": "test01"
}
class DatabaseManager:

    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None
        self.cursor = None

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
+----------------+--------------+------+-----+---------+----------------+
| Field          | Type         | Null | Key | Default | Extra          |
+----------------+--------------+------+-----+---------+----------------+
| question_id    | int          | NO   | PRI | NULL    | auto_increment |
| question_text  | varchar(255) | NO   |     | NULL    |                |
| option_a       | varchar(100) | NO   |     | NULL    |                |
| option_b       | varchar(100) | NO   |     | NULL    |                |
| option_c       | varchar(100) | NO   |     | NULL    |                |
| option_d       | varchar(100) | NO   |     | NULL    |                |
| correct_option | char(1)      | NO   |     | NULL    |                |
| category       | varchar(50)  | YES  |     | NULL    |                |
+----------------+--------------+------+-----+---------+----------------+

    Table : score_logs
+------------+-------------+------+-----+---------+----------------+
| Field      | Type        | Null | Key | Default | Extra          |
+------------+-------------+------+-----+---------+----------------+
| log_number | int         | NO   | PRI | NULL    | auto_increment |
| user_id    | int         | NO   | MUL | NULL    |                |
| category   | varchar(50) | YES  |     | NULL    |                |
| mark       | int         | NO   |     | NULL    |                |
+------------+-------------+------+-----+---------+----------------+

    Table : users
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| user_id    | int          | NO   | PRI | NULL    | auto_increment |
| username   | varchar(50)  | NO   |     | NULL    |                |
| password   | varchar(255) | NO   |     | NULL    |                |
| first_name | varchar(50)  | NO   |     | NULL    |                |
| last_name  | varchar(50)  | NO   |     | NULL    |                |
+------------+--------------+------+-----+---------+----------------+
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

        home.login_successful.connect(self.set_username)

    def GoToLogin(self):
        print("Successfully logged out")

        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def StartQuiz(self):
        print("Starting Quiz")

        # Create an instance of the RefreshMCQ class to fetch questions from the database
        refresh_mcq = RefreshMCQ(db_config)
        quiz_data_from_db = []
        refresh_mcq.add_questions_from_csv('questions.csv', quiz_data_from_db)

        # Pass the fetched quiz data to the Quiz class
        quiz = Quiz(quiz_data_from_db)
        widget.addWidget(quiz)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def set_username(self, username):
        self.l_user.setText(f"Welcome, {username}")

    def ViewUsername(self):
        current_username = self.l_user.text()
        if current_username == "Just Start the quiz":
            self.l_user.setText("")
        else:
            self.l_user.setText(f"Welcome, {current_username}")

# Login Page
class Login(QDialog):

    login_successful = pyqtSignal(str)

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
        try:
            with DatabaseManager(db_config) as db:  # Pass db_config here
                username = self.txt_uname.text()
                password = self.txt_pass.text()

                # the username already exists?
                query = "SELECT username, password FROM users WHERE username = %s"
                db.cursor.execute(query, (username,))
                user_data = db.cursor.fetchone()
                if user_data:
                    stored_password = user_data[1]

                    if password == stored_password:
                        self.login_successful.emit(username)  # Emit the signal with the username
                        home = Dashboard()
                        widget.addWidget(home)
                        widget.setCurrentIndex(widget.currentIndex() + 1)
                else:
                    print("Invalid username or password")

        except Exception as e:
            print("An error occurred:", str(e))

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

class RefreshMCQ:
    def __init__(self, db_config):
        self.db_config = db_config

    def fetch_questions(self, output_csv='questions.csv'):
        try:
            with DatabaseManager(self.db_config) as db:
                query = "SELECT * FROM mcq"
                db.cursor.execute(query)
                questions_data = db.cursor.fetchall()

                if questions_data:
                    self.write_to_csv(questions_data, output_csv)
                    print(f"Questions successfully written to {output_csv}")
                    return questions_data  # Return the fetched questions
                else:
                    print("No questions found in the database.")
                    return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    @staticmethod
    def write_to_csv(data, output_csv):
        with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Writing header
            writer.writerow(['question_id', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d',
                             'correct_option', 'category'])
            # Writing data
            writer.writerows(data)

    @staticmethod
    def add_questions_from_csv(file_path, quiz_data):
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    question_data = {
                        'question': row['question_text'],
                        'options': [row['option_a'], row['option_b'], row['option_c'], row['option_d']],
                        'answer': ord(row['correct_option'].lower()) - ord('a')
                        # Convert 'a', 'b', 'c', 'd' to 0, 1, 2, 3
                    }
                    quiz_data.append(question_data)
        except Exception as e:
            print(f"An error occurred: {str(e)}")


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
        print(f"Selected Option: {selected_option}, Correct Answer: {correct_answer}")

        if selected_option == correct_answer:
            self.score += 1
            print(f"Correct! Score: {self.score}")
        else:
            print("Incorrect.")

        self.current_question += 1
        self.show_question()  # Always display the next question or result, regardless of the answer

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
        msg.setText(f"Your score is: {self.score}/{len(self.quiz_data)}")

        # setting Message box window title
        msg.setWindowTitle("Question MessageBox")

        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok)

        # start the app
        retval = msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    refresh_mcq = RefreshMCQ(db_config)
    quiz_data_from_db = refresh_mcq.fetch_questions()

    if quiz_data_from_db:
        print("Fetched Questions:")
        for question in quiz_data_from_db:
            print(question)

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
