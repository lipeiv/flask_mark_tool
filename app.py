import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'


@app.route('/')
def index():
    with open('files.txt', 'r') as f:
        a = f.read()
    return render_template('index.html', value=a)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/work')
def workspace():
    img_dir = os.listdir('static/images')
    img_dir.reverse()
    with open("path_str.txt", "w") as f:
        f.writelines([path + "\n" for path in img_dir])
    return render_template('workspace.html')


@app.route('/space')
def space():
    return render_template('workspace.js')


@app.route('/img/<img_id>')
def space1(img_id):

    with open("path_str.txt", "r") as f:
        pic_list = f.readlines()

    for i in pic_list:
        i = i.replace('\n', '')
        with open("static/images/" + str(i), 'rb') as f:
            picture = f.read()

    return picture


if __name__ == '__main__':
    app.run(debug=True)
