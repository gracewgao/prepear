import psycopg2
import json

# connects to use the psycopg2 module
conn = psycopg2.connect(
    database='prepear',
    user='gracewgao',
    host='localhost',
    port=26257
)


conn.set_session(autocommit=True)
cur = conn.cursor()


def setup():
    cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS leetcode (id SERIAL PRIMARY KEY, name TEXT, difficulty TEXT, completed INT)")
    cur.execute("CREATE TABLE IF NOT EXISTS pears (id SERIAL PRIMARY KEY, username1 TEXT, username2 TEXT)")

    with open("bot/leetcode.json") as f:
        levels = json.load(f)
        for level in levels:
            for q in level:
                cur.execute(f"UPSERT INTO leetcode (name, difficulty, completed) VALUES ('{q}', '{level}', 0) RETURNING id")


def make_pear(user1, user2):
    pear_id = cur.execute(f"UPSERT INTO leetcode (username1, username2) VALUES ('{user1}', '{user2}') RETURNING id")
    return pear_id

def get_question(difficulty):
    cur.execute(f"SELECT name from leetcode WHERE difficulty='{difficulty}'")
    questions = cur.fetchall()

    # todo: check if user has already done it 
    rand = random.randint(0, len(questions) - 1)
    name = questions[rand]
    pear = make_pear('gracewgao', 'bonnie')

    leetcode_url = 'https://leetcode.com/problems/' + name + '/'
    code_url = 'https://codeshare.io/prepear-' + name + '-' + pear

    message = f'Try this one!\n{leetcode_url}\nYou can get started here:\n{code_url}'

    return name


def add_user(username):
    cur.execute(f"UPSERT INTO users (username) VALUES ('{username}') RETURNING id")


def get_users():
    cur.execute("SELECT id, username FROM users")
    users = cur.fetchall()
    return users

setup()
add_user('gracewgao')
users = get_users()

for row in users:
    print([str(cell) for cell in row])

cur.close()
conn.close()