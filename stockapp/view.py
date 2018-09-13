from flask import render_template, Flask, request, redirect
from stockapp.get_data import get_stock_data
import json

app = Flask(__name__)
# 接收方式为post和get
@app.route('/', methods=["POST", "GET"])
def homepage():
    try:
        if request.method == 'POST':        #接收post数据
            search = request.form['search']         # 获取name为search的表单数据
            data, stock_name, header = get_stock_data(search)        #
            if data:
                return render_template("main.html", data=json.dumps(data), stock_name=stock_name, header=json.dumps(header))  # 将数据传递给网页
            else:
                return render_template('main.html', sign='没有查到该股票')
        else:
            return render_template('main.html')
    except Exception as e:
        return render_template("main.html", sign=e)

