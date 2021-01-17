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

    cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username TEXT, waiting INT)")
    cur.execute("CREATE TABLE IF NOT EXISTS leetcode (id SERIAL PRIMARY KEY, name TEXT, difficulty TEXT, completed INT)")
    cur.execute("CREATE TABLE IF NOT EXISTS languages (user_id SERIAL PRIMARY KEY, language TEXT)")

    with open("bot/leetcode.json") as f:
        levels = json.load(f)
        for level in levels:
            for q in levels[level]:
                cur.execute(f"UPSERT INTO leetcode (name, difficulty, completed) VALUES ('{q}', '{level}', 0) RETURNING id")


def add_user(username):
    cur.execute(f"UPSERT INTO users (username) VALUES ('{username}') RETURNING id")


def add_language(user_id, language):
     cur.execute(f"INSERT INTO (user_id, language) VALUES ('{user_id}', '{language}')")


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


def add_to_queue(username, difficulty):
    cur.execute(f"UPDATE users SET waiting={difficulty} WHERE id='{username}'")


# makes pear if possible, otherwise adds to waiting list
def check_pear(username, difficulty):

    cur.execute(f"SELECT id from users WHERE username='{username}'")
    user_id = cur.fetchone()
    ref_set = get_languages(user_id)

    cur.execute(f"SELECT id, username from users WHERE waiting='{difficulty}'")
    users = cur.fetchall()

    for user in users:
        match_set = get_languages(user[0])
        # if there are matching languages, pairs them up
        if ref_set.intersection(match_set):
            # makes pairing
            pass
        else:
            add_to_queue(username, difficulty)


def get_languages():
    cur.execute(f"SELECT language from languages WHERE user_id='{user_id}' GROUP BY user_id")
    languages = cur.fetchall()
    lang_set = set(languages)
    return lang_set


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

users = get_users()
questions = get_questions()