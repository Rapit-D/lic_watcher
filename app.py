from flask import Flask, render_template, request
from flask_moment import Moment


app = Flask(__name__)


@app.route('/')
def hello_world():
    context = [{
        'index': 1,
        'port': '5800',
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


@app.route('/watchedlist', methods={"POST", "GET"})  # 添加/删除license 服务器
def setting():
    data = request.get_json
    print(data)
    return render_template('watchedlist.html')
