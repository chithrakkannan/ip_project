import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QLabel, QPushButton

class Quiz(QDialog):
    def __init__(self, quiz_data):
        super(Quiz, self).__init__()

        self.quiz_data = quiz_data
        self.current_question = 0
        self.score = 0

        # Load the UI from the "quiz.ui" file
        loadUi("quiz.ui", self)

        # Connect button clicks to the corresponding functions
        self.btn_01.clicked.connect(lambda: self.check_answer(0))
        self.btn_02.clicked.connect(lambda: self.check_answer(1))
        self.btn_03.clicked.connect(lambda: self.check_answer(2))
        self.btn_04.clicked.connect(lambda: self.check_answer(3))

        # Initialize the quiz
        self.show_question()

    def show_question(self):
        if self.current_question < len(self.quiz_data):
            question_data = self.quiz_data[self.current_question]

            self.l_question.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
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
        result = Scores(self.score)
        widget.addWidget(result)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Scores(QDialog):
    def __init__(self, score):
        super(Scores, self).__init__()

        self.setWindowTitle("Quiz Results")
        self.setGeometry(200, 200, 300, 200)

        self.layout = QVBoxLayout()

        label = QLabel("Quiz Completed")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))

        score_label = QLabel(f"Your Score: {score}")
        score_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        restart_button = QPushButton("Restart Quiz")
        restart_button.clicked.connect(self.restart_quiz)

        self.layout.addWidget(label)
        self.layout.addWidget(score_label)
        self.layout.addWidget(restart_button)

        self.setLayout(self.layout)

    def restart_quiz(self):
        quiz = Quiz(quiz_data)
        widget.addWidget(quiz)
        widget.setCurrentIndex(widget.currentIndex() + 1)

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
    widget = QtWidgets.QStackedWidget()
    quiz = Quiz(quiz_data)
    widget.addWidget(quiz)
    widget.setFixedHeight(700)
    widget.setFixedWidth(1200)
    widget.show()
    sys.exit(app.exec_())

########################################################################################################################





