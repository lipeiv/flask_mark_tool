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
page = 1


@app.route('/', methods=["GET", "POST"])
def index():
    global width
    global height
    global page

    # img_url = "http://www.html5canvastutorials.com/demos/assets/darth-vader.jpg"
    with open("img_path.txt", 'r') as f:

        img_dir = linecache.getline("img_path.txt", page).replace("\n", "")
        # a = int(f.read())
        img_url = "static/images/" + img_dir
        if page > len(img_dir)-2:
            page = 1
        else:
            page += 1
        print(page)

    print("'" + img_url + "'")
    im = cv2.imread(img_url)
    width = im.shape[1]
    height = im.shape[0]

    print(width)
    print(height)
    # with open("files.txt", 'w')as f:
    #     f.write(str(a))
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
    width = 900
    height = 500

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

    x = round(x0 / width, 6)
    y = round(y0 / height, 6)

    result = [category, x, y, round(w/width, 6), round(h/height, 6)]
    result = str(result).replace("[", "").replace("]", "").replace("'", "").replace(",", "")
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


@app.route('/mark/static/images/<img_id>.jpg', methods=["GET"])
def mark(img_id):
    global width
    global height
    text = []
    with open('static/text/'+img_id+'.txt', 'rb')as f:
        text1 = f.read()
    print(text1)
    return text1


@app.route('/space', methods=["GET"])
def space():
    global width
    global height
    # 图片路径
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
    print(img_dir0)

    # 渲染图片路径与标签
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
                           )


if __name__ == '__main__':
    app.run(debug=True)
