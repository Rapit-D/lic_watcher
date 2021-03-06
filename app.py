from functions.lic_validator import home_page_schema, sql_query_schema, pprint, ServerSchema, srv_features_schema, srv_features_schemas, current_lic_usage
from functions.json_loader import json_loader
from functions import his_data
from functions.log_parser import log_parser
from flask import Flask, render_template, request, redirect, Blueprint
import os


app = Flask(__name__)


@app.route("/")
def hello_world():
    # 主页
    return render_template("home.html")


@app.route("/get_server_info")
def get_server_info():
    # 主页表格数据API
    with open("static/server_info/home_page.json", "r") as f:
        server_info = f.read()
        result = home_page_schema.loads(server_info)
        result = home_page_schema.dumps(result)
        f.close()
    return result


@app.route("/watchedlist", methods={"POST", "GET"})
def setting():
    # 添加/删除license 服务器
    if request.method == "POST":
        data = request.json
        result = ServerSchema().load(data)
        with open("static/server_info/home_page.json", "r") as f:
            server_info = f.read()
            result = home_page_schema.loads(server_info)
            f.close()

        result.append(data)

        with open("static/server_info/home_page.json", 'w') as f:
            json_data = home_page_schema.dumps(result)
            f.write(json_data)
            f.close()
        return render_template("watchedlist.html")
    else:
        return render_template("watchedlist.html")


@app.route("/historical_data")
def historical_data():
    return render_template("historical_data.html")


@app.route("/chart_data", methods={'GET', 'POST'})
def chart_data():
    if request.method == 'POST':
        data = request.json

        data = his_data.sql_data(min_date=data['start_date'].split('T')[
                                 0], max_date=data['end_date'].split('T')[0], server=data['srvs'], feature=data['features'])

    elif request.method == 'GET':
        data = his_data.sql_data()
    result = sql_query_schema.dumps(data)
    return result


@app.route("/srv_features_info", methods={"post"})
def srv_features_info():
    data = request.json
    _files = []
    for item in data['servers']:
        _files.append('static/server_info/' + item + '_features.json')
    result = []
    for item in _files:
        result.append(srv_features_schema.loads(json_loader(item)))
    result = srv_features_schemas.dumps(result)
    return result


@app.route("/current_usage", methods={"get"})
def current_usage():
    return render_template("current_usage.html")


@app.route("/get_current_feature_status", methods={"post"})
def get_current_feature_status():
    data = request.json
    current_dir = os.path.abspath(os.path.dirname(__file__))
    log_file = os.path.join(
        current_dir, f'static/server_info/{data["srvs"]}.log')
    result = []
    parser = log_parser(log_file, 'Users')
    data = parser.user_checked_info()

    for item in parser.user_checked_info():
        result.append(item)
    result = current_lic_usage.dumps(result)
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
