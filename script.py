from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

class Quiz:
    def __init__(self):
        self.total_questions = 10
        self.correct_answers = 0
        self.question_counter = 0
        self.current_numbers = None

    def generate_numbers(self):
        num1 = random.randint(1, 12)
        num2 = random.randint(1, 12)
        return num1, num2

    def reset_quiz(self):
        self.correct_answers = 0
        self.question_counter = 0
        self.current_numbers = None

quiz_instance = Quiz()

@app.route('/')
def index():
    quiz_instance.reset_quiz()
    return render_template('index.html')

@app.route('/quiz', methods=['POST', 'GET'])
def quiz():
    if request.method == 'GET':
        if quiz_instance.current_numbers is None:
            quiz_instance.current_numbers = quiz_instance.generate_numbers()

        num1, num2 = quiz_instance.current_numbers
        question = f"Vad är {num1} x {num2}?"
        return render_template('quiz.html', question=question)

    if request.method == 'POST':
        if 'user_answer' in request.form:
            if quiz_instance.current_numbers is None:
                return redirect(url_for('index'))

            user_answer = int(request.form['user_answer'])
            num1, num2 = quiz_instance.current_numbers
            correct_answer = num1 * num2

            if user_answer == correct_answer:
                quiz_instance.correct_answers += 1

            quiz_instance.question_counter += 1
            quiz_instance.current_numbers = None

            if quiz_instance.question_counter < quiz_instance.total_questions:
                return redirect(url_for('quiz'))
            else:
                return redirect(url_for('result'))

    return redirect(url_for('index'))

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        return redirect(url_for('quiz'))

    return render_template('result.html', correct_answers=quiz_instance.correct_answers, total_questions=quiz_instance.total_questions)

if __name__ == '__main__':
    app.run(debug=True)
