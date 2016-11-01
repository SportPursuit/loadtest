from flask import Flask
app = Flask(__name__)

users = ['dermot.osullivan+test@sportpursuit.co.uk', 'dermot.osullivan+test1@sportpursuit.co.uk']
used = []

@app.route('/')
def get():
    user = (set(users) - set(used)).pop()
    used.append(user)
    return user


@app.route('/<user>')
def release(user):
    used.remove(user)
    return 'success'


if __name__ == '__main__':
    app.run()