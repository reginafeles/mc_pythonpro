import sqlite3
db_name = 'quiz.db'
conn = None
cursor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    ''' удаляет все таблицы '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

    
def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')

    query = '''CREATE TABLE IF NOT EXISTS question (
        id INTEGER PRIMARY KEY,
        question VARCHAR,
        answer VARCHAR,
        wrong1 VARCHAR,
        wrong2 VARCHAR,
        wrong3 VARCHAR)'''
    do(query)

    query = '''CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY,
        name VARCHAR
        )'''
    do(query)

    query = '''CREATE TABLE IF NOT EXISTS quiz_content (
        id INTEGER PRIMARY KEY,
        quiz_id INTEGER,
        question_id INTEGER,
        FOREIGN KEY (quiz_id) REFERENCES quiz (id)
        FOREIGN KEY (question_id) REFERENCES question (id))'''
    do(query)

    cursor.close()
    conn.close()

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

quizes = [('Своя игра',), ('Кто хочет стать миллионером',), ('Самый умный',)]

def addquiz():
    open()
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.commit()
    close()

questions = [
        ('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного', 'Два'),
        ('Каким станет зеленый утес, если упадет в Красное море?', 'Мокрым', 'Красным', 'Не изменится', 'Фиолетовым'),
        ('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
        ('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море', 'Воздух'),
        ('Когда сетью можно вытянуть воду?', 'Когда вода замерзла', 'Когда нет рыбы', 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
        ('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако')]

def addquestion():
    open()
    cursor.executemany('''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)''', questions)
    conn.commit()
    close()

def addrelation():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    query = '''INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)'''
    while input('Add relation? (y/n)') != 'n':
        question_id = int(input('ID question:'))
        quiz_id = int(input('ID quiz'))
        cursor.execute(query, [quiz_id, question_id])
    conn.commit()
    close()

def get_question_after(question_id, quiz_id):
    open()
    query = '''SELECT 
    quiz_content.id, question.question, 
    question.answer, question.wrong1, 
    question.wrong2, question.wrong3 
    FROM question, quiz_content
    WHERE quiz_content.question_id == question.id
    AND quiz_content.id > ? 
    AND quiz_content.quiz_id == (?)'''
    cursor.execute(query, [question_id, quiz_id])
    result = cursor.fetchall()
    close()
    if result:
        return result[0]
    else:
        return None

def get_quizes():
    open()
    query = '''SELECT * FROM quiz ORDER BY id'''
    cursor.execute(query)
    data = cursor.fetchall()
    close()
    return data

def check_answer(question_id, answer):
    query = '''
    SELECT question.answer FROM quiz_content, question WHERE quiz_content.id = ?
    AND quiz_content.question_id = question.id
    '''
    open()
    cursor.execute(query, str(question_id))
    result = cursor.fetchone()
    close()
    if result[0] == answer:
        return True
    else:
        return False

def main():
    clear_db()
    create()   
    addquiz()
    addquestion() 
    addrelation()
    show_tables()
    get_quizes()

if __name__ == "__main__":
    main()
