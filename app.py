from flask import Flask,render_template
app = Flask(__name__)


@app.route('/<t>')
def hello_world(t=None):
    return render_template('base.html', t=t)
