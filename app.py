import json
import linecache
import os
import cv2
from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'
img_dir = os.listdir('static/images')
with open("img_path.txt", "w")as f:
    f.writelines(i + "\n" for i in img_dir)

width = 0
height = 0
page = 0


@app.route('/', methods=["GET", "POST"])
def index():
    img_url = "http://www.html5canvastutorials.com/demos/assets/darth-vader.jpg"
    with open("files.txt", 'r') as f:
        a = int(f.read())
        img_url = "/static/images/" + img_dir[a]
        if a > len(img_dir)-2:
            a = 0
        else:
            a += 1
        print(a)
    with open("files.txt", 'w')as f:
        f.write(str(a))
    return render_template('work.html', img_url=img_url)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/work', methods=["GET"])
def workspace():

    return render_template('workspace.html')


@app.route('/work', methods=["POST"])
def work_delete():
    global width
    global height

    data_ = request.get_data(as_text=True)
    data = json.loads(data_)
    pic_id = data.get("img_id").strip("/static/images .jpg")
    category = data.get("category_id")
    point = data.get("point")
    x0 = point[0][0]
    y0 = point[0][1]
    x1 = point[2][0]
    y1 = point[2][1]

    w = x1 - x0
    h = y1 - y0

    x = x0 / width
    y = y0 / height

    result = [category, x, y, w/width, h/height]
    result = str(result).replace("[", "").replace("]", "").replace("'", "")
    print(result)

    with open("static/text/"+pic_id+".txt", 'a+', encoding="utf-8") as f:
        f.write(result+'\n')
    return "200 OK"


@app.route('/work', methods=["DELETE"])
def work_post():
    data_ = request.get_data(as_text=True)
    data = json.loads(data_)
    img_id = data.get("img_id").strip("/static/images/ .jpg")
    index = data.get("index")+1
    print("img_id:" + img_id + " index:"+str(index))
    return "200 OK"


@app.route('/space', methods=["GET"])
def space():
    global page
    img_dir0 = 'static/images/' + linecache.getline("img_path.txt", 1 + page*10).replace("\n", "")
    img_dir1 = 'static/images/' + linecache.getline("img_path.txt", 2 + page*10).replace("\n", "")
    img_dir2 = 'static/images/' + linecache.getline("img_path.txt", 3 + page*10).replace("\n", "")
    img_dir3 = 'static/images/' + linecache.getline("img_path.txt", 4 + page*10).replace("\n", "")
    img_dir4 = 'static/images/' + linecache.getline("img_path.txt", 5 + page*10).replace("\n", "")
    img_dir5 = 'static/images/' + linecache.getline("img_path.txt", 6 + page*10).replace("\n", "")
    img_dir6 = 'static/images/' + linecache.getline("img_path.txt", 7 + page*10).replace("\n", "")
    img_dir7 = 'static/images/' + linecache.getline("img_path.txt", 8 + page*10).replace("\n", "")
    img_dir8 = 'static/images/' + linecache.getline("img_path.txt", 9 + page*10).replace("\n", "")
    img_dir9 = 'static/images/' + linecache.getline("img_path.txt", 10 + page*10).replace("\n", "")

    if page > len(img_dir) / 10 - 1:
        page = 0
    else:
        page += 1
    im = cv2.imread(img_dir0)
    global width
    global height

    width = im.shape[1]
    height = im.shape[0]
    # with open(img_dir0, "r", encoding="utf-8") as f:
    #     mark0 = f.readlines()
    #     print(mark0)
    # with open(img_dir1, "r") as f:
    #     mark1 = f.readlines()
    # with open(img_dir2, "r") as f:
    #     mark2 = f.readlines()
    # with open(img_dir3, "r") as f:
    #     mark3 = f.readlines()
    # with open(img_dir4, "r") as f:
    #     mark4 = f.readlines()
    # with open(img_dir5, "r") as f:
    #     mark5 = f.readlines()
    # with open(img_dir6, "r") as f:
    #     mark6 = f.readlines()
    # with open(img_dir7, "r") as f:
    #     mark7 = f.readlines()
    # with open(img_dir8, "r") as f:
    #     mark8 = f.readlines()
    # with open(img_dir9, "r") as f:
    #     mark9 = f.readlines()

    return render_template('workspace.js',
                           img_id0=img_dir0,
                           img_id1=img_dir1,
                           img_id2=img_dir2,
                           img_id3=img_dir3,
                           img_id4=img_dir4,
                           img_id5=img_dir5,
                           img_id6=img_dir6,
                           img_id7=img_dir7,
                           img_id8=img_dir8,
                           img_id9=img_dir9,
                           # mark0=mark0,
                           # mark1=mark1,
                           # mark2=mark2,
                           # mark3=mark3,
                           # mark4=mark4,
                           # mark5=mark5,
                           # mark6=mark6,
                           # mark7=mark7,
                           # mark8=mark8,
                           # mark9=mark9,
                           )


if __name__ == '__main__':
    app.run(debug=True)
