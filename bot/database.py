import psycopg2
import json
import random

# connects to use the psycopg2 module
conn = psycopg2.connect(
    database='prepear',
    user='gracewgao',
    host='localhost',
    port=26257
)

conn.set_session(autocommit=True)
cur = conn.cursor()

def setup_db():

    cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS leetcode (id SERIAL PRIMARY KEY, name TEXT, difficulty TEXT, completed INT)")
    
    with open("bot/leetcode.json") as f:
        levels = json.load(f)
        for level in levels:
            for q in levels[level]:
                cur.execute(f"UPSERT INTO leetcode (name, difficulty, completed) VALUES ('{q}', '{level}', 0) RETURNING id")


def get_question(difficulty):
    cur.execute(f"SELECT name, completed from leetcode WHERE difficulty='{difficulty}'")
    questions = cur.fetchall()

    # todo: check if user has already done it 
    rand = random.choice(questions)
    name = rand[0]
    count = rand[1]

    leetcode_url = 'https://leetcode.com/problems/' + name + '/'
    code_url = 'https://codeshare.io/prepear-' + name + '-' + str(count)

    message = f'Try this one!\n{leetcode_url}\n\nYou can get started here:\n{code_url}'

    return message


def add_user(username):
    cur.execute(f"UPSERT INTO users (username) VALUES ('{username}') RETURNING id")


def get_users():
    cur.execute("SELECT id, username FROM users")
    users = cur.fetchall()
    return users


def get_questions():
    cur.execute("SELECT name, difficulty, completed FROM leetcode")
    questions = cur.fetchall()
    return questions


def close_db():
    cur.close()
    conn.close()


setup_db()
add_user('gracewgao')
users = get_users()
questions = get_questions()

for row in users:
    print([str(cell) for cell in row])

for row in questions:
    print([str(cell) for cell in row])