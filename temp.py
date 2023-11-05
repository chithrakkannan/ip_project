import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QRadioButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt

class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Quiz")
        self.setGeometry(100, 100, 800, 400)

        self.quiz_data = [
            {
                'question': "What is the capital of France?",
                'options': ["London", "Madrid", "Paris", "Berlin"],
                'answer': "Paris"
            },
            {
                'question': "Which language is this quiz written in?",
                'options': ["Python", "Java", "C++", "JavaScript"],
                'answer': "Python"
            },
            {
                'question': "What is 2 + 2?",
                'options': ["3", "4", "5", "6"],
                'answer': "4"
            }
            # Add more questions here
        ]

        self.current_question = 0
        self.score = 0

        self.setup_ui()
        self.show_question()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        self.option_buttons = []
        for i in range(4):
            option_button = QRadioButton()
            self.option_buttons.append(option_button)
            self.layout.addWidget(option_button)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.submit_button)

        self.central_widget.setLayout(self.layout)

    def show_question(self):
        if self.current_question < len(self.quiz_data):
            question_data = self.quiz_data[self.current_question]
            self.question_label.setText(question_data['question'])
            options = question_data['options']
            for i in range(4):
                self.option_buttons[i].setText(options[i])
                self.option_buttons[i].setEnabled(True)
            self.submit_button.setEnabled(True)
        else:
            self.question_label.setText("Quiz complete! Your score is: {}".format(self.score))
            for button in self.option_buttons:
                button.setEnabled(False)
            self.submit_button.setEnabled(False)

    def check_answer(self):
        selected_option = None
        for i in range(4):
            if self.option_buttons[i].isChecked():
                selected_option = self.option_buttons[i].text()
                break

        if selected_option == self.quiz_data[self.current_question]['answer']:
            self.score += 1

        self.current_question += 1
        self.show_question()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec_())
