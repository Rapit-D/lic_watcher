from flask import Flask, render_template, request, redirect
from flask_moment import Moment
from marshmallow import Schema, fields, ValidationError, pprint


app = Flask(__name__)


@app.route('/')
def hello_world():
    # 主页
    return render_template('home.html')


@app.route('/get_server_info')
def get_server_info():
    # 主页表格数据API
    with open('static/server_info/servers.json', 'r') as f:
        server_info = f.read()
        serverschema = ServerSchema(many=True)
        result = serverschema.loads(server_info)
        result = serverschema.dumps(result)
        f.close()
    return result


@app.route('/watchedlist', methods={"POST", "GET"})
def setting():
    # 添加/删除license 服务器
    if request.method == "POST":
        data = request.json
        result = ServerSchema().load(data)
        with open("static/server_info/servers.json", "r") as f:
            server_info = f.read()
            serverschema = ServerSchema(many=True)
            result = serverschema.loads(server_info)
            f.close()

        result.append(data)

        with open("static/server_info/servers.json", 'w') as f:
            json_data = serverschema.dumps(result)
            f.write(json_data)
            f.close()
        return render_template('watchedlist.html')
    else:
        return render_template('watchedlist.html')


def validate_portnumber(n):
    # 验证portnumber 的值
    if n <= 0:
        raise ValidationError("Port number should reside between 1 ~ 65535")
    elif n >= 65535:
        raise ValidationError("Port number should reside between 1 ~ 65535")


class ServerSchema(Schema):
    # 验证前端传来的数据
    portnumber = fields.Integer(required=True, validate=validate_portnumber)
    server = fields.String(required=True)
    description = fields.String()
    location = fields.String(required=True)
    status = fields.String()
    version = fields.String()


@app.route("/test", methods={'post'})
def test():
    data = request.json
    dataty = type(data)
    return render_template('test.html', data=data, dataty=dataty)
