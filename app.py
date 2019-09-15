import json
import linecache
import os
from PIL import Image
from flask import Flask, render_template, request, make_response
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'

img_dir = os.listdir('static/images')
with open("img_path.txt", "w")as f:
    f.writelines(i + "\n" for i in img_dir)


@app.route('/', methods=["GET", "POST"])
def index():
    page =1
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
    im = Image.open(img_url)
    print(im.size)
    # width = im.shape[1]
    # height = im.shape[0]

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
    data_ = request.get_data(as_text=True)
    data = json.loads(data_)
    img_dir = data.get("img_id")
    img_id = img_dir.strip("/static/images .jpg")
    category = data.get("category_id")

    # 前端返回的坐标值
    point = data.get("point")
    x0 = point[0][0]
    y0 = point[0][1]
    x1 = point[2][0]
    y1 = point[2][1]
    w = x1 - x0
    h = y1 - y0

    # 读取图片实际像素
    im = Image.open(img_dir.strip("/"))
    width_height = im.size
    width_ = width_height[0]
    height_ = width_height[1]
    print(width_)
    print(height_)

    # 定位
    if width_/height_ > 900/500:
        print("宽图")
        x = round(x0 / 900, 6)
        y = round((y1 - (500 - height_) / 2) / 500, 6)
        width = round(w / 810000, 6)
        height = round(h * h / 900, 6)
    else:
        print("长图")
        x = round((x0 - (900 - width_) / 2 + 20) / 900, 6)
        y = round(y0 / 500, 6)
        height = round(h / 500, 6)
        width = round(w * h / 250000, 6)

    result = [category, x, y, width, height]
    result = str(result).replace("[", "").replace("]", "").replace("'", "").replace(",", "")
    print(result)

    with open("static/text/"+img_id+".txt", 'a+', encoding="utf-8") as f:
        f.write(result+'\n')
    return "200 POST OK"


@app.route('/work', methods=["DELETE"])
def work_post():
    data_ = request.get_data(as_text=True)
    data = json.loads(data_)
    img_id = data.get("img_id").strip("/static/images/ .jpg")
    point = data.get("point")
    print(img_id)
    print(point)
    return "200 DELETE OK"


@app.route('/mark/static/images/<img_id>.jpg', methods=["GET"])
def mark(img_id):
    with open('static/text/'+img_id+'.txt', 'rb')as f:
        text1 = f.read()
    print(text1)
    return text1


@app.route('/space', methods=["GET"])
def space():
    # 图片路径
    global img_dir
    page = request.cookies.get('page')
    if page is None:
        page = "0"
    page = int(page)
    if page > len(img_dir) / 10:
        page = 0

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
    page += 1
    arr = []

    # arr.append()


    # 渲染图片路径与标签
    resp = make_response(render_template('workspace.js',
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
                           arr=[[0, 6, [[221, 92], [390, 92], [390, 200], [221, 200], [221, 92]]],
                                [1, 3, [[321, 292], [490, 292], [490, 400], [321, 400], [321, 292]]]

                               ],
                           ))
    resp.set_cookie("page", str(page))
    return resp


if __name__ == '__main__':
    app.run(debug=True)
