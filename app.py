from flask import Flask, render_template, request, redirect, Blueprint
from .lic_validator import ServerSchema, validate_portnumber
from .DB import session
from .chart_data import chart_data

app = Flask(__name__)


@app.route("/")
def hello_world():
    # 主页
    return render_template("home.html")


@app.route("/get_server_info")
def get_server_info():
    # 主页表格数据API
    with open("static/server_info/servers.json", "r") as f:
        server_info = f.read()
        serverschema = ServerSchema(many=True)
        result = serverschema.loads(server_info)
        result = serverschema.dumps(result)
        f.close()
    return result


@app.route("/watchedlist", methods={"POST", "GET"})
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
        return render_template("watchedlist.html")
    else:
        return render_template("watchedlist.html")


@app.route("/test", methods={"post"})
def test():
    data = request.json
    dataty = type(data)
    return render_template("test.html", data=data, dataty=dataty)


@app.route("/historical_data")
def historical_data():
    return render_template("historical_data.html")


@app.route("/chart_data", methods={'GET'})
def chart_data():

    sql, params = chart_data(min_date='2020-06-10', max_date='2020-06-11',
                             server=['5280@SZ-glblic01',
                                     '5280@nl1lic01.vas.goodix.com'],
                             feature=['111', 'Capture_CIS_Studio'])
    data = session.execute(sql, params)
    print(data.fetchone())
    return data