from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

total_questions = 10
correct_answers = 0
question_counter = 0
current_numbers = None  # Variable to store the current numbers

def generate_numbers():
    num1 = random.randint(1, 12)
    num2 = random.randint(1, 12)
    return num1, num2

@app.route('/')
def index():
    global correct_answers
    global question_counter
    global current_numbers

    # Reset global variables
    correct_answers = 0
    question_counter = 0
    current_numbers = None

    return render_template('index.html')

@app.route('/quiz', methods=['POST', 'GET'])
def quiz():
    global correct_answers
    global question_counter
    global current_numbers

    if request.method == 'GET':
        if current_numbers is None:
            current_numbers = generate_numbers()

        num1, num2 = current_numbers
        question = f"Vad är {num1} gånger {num2}?"
        return render_template('quiz.html', question=question)

    if request.method == 'POST':
        if 'user_answer' in request.form:
            if current_numbers is None:
                return redirect(url_for('index'))

            user_answer = int(request.form['user_answer'])
            num1, num2 = current_numbers
            correct_answer = num1 * num2

            if user_answer == correct_answer:
                correct_answers += 1

            question_counter += 1
            current_numbers = None

            if question_counter < total_questions:
                return redirect(url_for('quiz'))
            else:
                return redirect(url_for('result'))

    return redirect(url_for('index'))

@app.route('/result', methods=['GET', 'POST'])
def result():
    global correct_answers
    global question_counter

    if request.method == 'POST':
        # Redirect to the quiz route, which resets the variables
        return redirect(url_for('quiz'))

    return render_template('result.html', correct_answers=correct_answers, total_questions=total_questions)

if __name__ == '__main__':
    app.run(debug=True)
