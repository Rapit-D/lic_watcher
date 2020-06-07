from flask import Flask, render_template, request, redirect
from flask_moment import Moment
from marshmallow import Schema, fields, ValidationError


app = Flask(__name__)


@app.route('/')
def hello_world():
    context = [{
        'index': 1,
        'port': "5800",
        'server': 'sz-glblic01',
        'description': 'Cadence Server',
        'status': 'UP',
        'version': '10.16.13',
        'country': 'cn'
    },
        {
        'index': 2,
        'port': '27020',
        'server': 'sz-glblic01',
        'description': 'Synopls',
        'status': 'UP',
        'version': '200.1.3',
        'country': 'nl'
    }
    ]
    return render_template('home.html', data=context)


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
