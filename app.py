from flask import Flask, render_template, request, redirect
from flask_moment import Moment
from marshmallow import Schema, fields, ValidationError, pprint


app = Flask(__name__)

"""
主页
"""


@app.route('/')
def hello_world():
    return render_template('home.html')


"""
主页表格数据API
"""


@app.route('/get_server_info')
def get_server_info():
    with open('static/server_info/servers.json', 'r') as f:
        server_info = f.read()
        serverschema = ServerSchema(many=True)
        result = serverschema.loads(server_info)
        result = serverschema.dumps(result)
        f.close()
    return result


"""
添加/删除license 服务器
"""


@app.route('/watchedlist', methods={"POST", "GET"})
def setting():
    if request.method == "POST":
        data = request.json
        try:
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
        except Exception as err:
            print(err.messages)
        return render_template('watchedlist.html')
    else:
        return render_template('watchedlist.html')


"""
验证前端传来的数据
"""


def validate_portnumber(n):
    # 验证portnumber 的值
    if n <= 0:
        raise ValidationError("Port number should reside between 1 ~ 65535")
    elif n >= 65535:
        raise ValidationError("Port number should reside between 1 ~ 65535")


class ServerSchema(Schema):
    portnumber = fields.Integer(required=True, validate=validate_portnumber)
    server = fields.String(required=True)
    description = fields.String()
    location = fields.String(required=True)
