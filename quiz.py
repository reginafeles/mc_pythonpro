from flask import Flask, redirect, url_for, session, request, render_template
from db_scripts import get_question_after, get_quizes, check_answer
from random import shuffle
import os

def index():
    if request.method == 'GET':
        start_quiz(-1)
        return quiz_form()
    if request.method == 'POST':
        question_id = request.form.get('quiz')
        start_quiz(question_id)
        return redirect(url_for('test'))

def start_quiz(quiz_id):
    session['quiz_n'] = quiz_id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0

def quiz_form():
    q_list = get_quizes()
    return render_template('start.html', q_list=q_list)

def end_quiz():
    session.clear()

def save_answers():
    answer = request.form.get('ans_text')
    question_id = request.form.get('q_id')
    session['last_question'] = question_id
    session['total'] += 1
    if check_answer(question_id, answer):
        session['answers'] += 1

def test():
    if (not 'quiz_n' in session) or int(session['quiz_n']) < 0:
        return redirect(url_for('index'))

    else:
        if request.method == 'POST':
            save_answers()

        result = get_question_after(session['last_question'], session['quiz_n'])
        if result is None or len(result) == 0:
            return redirect(url_for('result'))
        else:
            session['last_question'] = result[0]
            answers_list = [result[2], result[3], result[4], result[5]]
            shuffle(answers_list)
            return render_template('test.html', question=result[1], question_id=result[0], answers_list=answers_list)

def result():
    return render_template('result.html', ans=str(session['answers']))
    end_quiz()

folder = os.getcwd()

app = Flask(__name__, static_folder=folder, template_folder=folder)
app.config['SECRET_KEY']='AaBbCc132'
app.add_url_rule('/', 'index', index, methods=['post', 'get'])
app.add_url_rule('/test', 'test', test, methods=['post', 'get'])
app.add_url_rule('/result', 'result', result)

if __name__ == "__main__":
    app.run()