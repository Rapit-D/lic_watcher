from flask import Flask, render_template
from flask_moment import Moment

app = Flask(__name__)


@app.route('/home')
def hello_world():
    context = [{
        'index': 1,
        'port': 5800,
        'server': 'sz-glblic01',
        'description': 'Cadence Server',
        'status': 'UP',
        'version': '10.16.13'
    },
        {
        'index': 2,
        'port': 27020,
        'server': 'sz-glblic01',
        'description': 'Synopls',
        'status': 'UP',
        'version': '200.1.3'
    }
        #     {
        #     'index': 2,
        #     'port': 27020,
        #     'server': 'sz-glblic01',
        #     'description': 'Synopls',
        #     'status': 'UP',
        #     'version': '200.1.3'
        # },
        #     {
        #     'index': 2,
        #     'port': 27020,
        #     'server': 'sz-glblic01',
        #     'description': 'Synopls',
        #     'status': 'UP',
        #     'version': '200.1.3'
        # },
        #     {
        #     'index': 2,
        #     'port': 27020,
        #     'server': 'sz-glblic01',
        #     'description': 'Synopls',
        #     'status': 'UP',
        #     'version': '200.1.3'
        # },
        #     {
        #     'index': 2,
        #     'port': 27020,
        #     'server': 'sz-glblic01',
        #     'description': 'Synopls',
        #     'status': 'UP',
        #     'version': '200.1.3'
        # },
        #     {
        #     'index': 2,
        #     'port': 27020,
        #     'server': 'sz-glblic01',
        #     'description': 'Synopls',
        #     'status': 'UP',
        #     'version': '200.1.3'
        # },
        #     {
        #     'index': 2,
        #     'port': 27020,
        #     'server': 'sz-glblic01',
        #     'description': 'Synopls',
        #     'status': 'UP',
        #     'version': '200.1.3'
        # },
        #     {
        #     'index': 2,
        #     'port': 27020,
        #     'server': 'sz-glblic01',
        #     'description': 'Synopls',
        #     'status': 'UP',
        #     'version': '200.1.3'
        # },
        #     {
        #     'index': 2,
        #     'port': 27020,
        #     'server': 'sz-glblic01',
        #     'description': 'Synopls',
        #     'status': 'UP',
        #     'version': '200.1.3'
        # },
        #     {
        #     'index': 2,
        #     'port': 27020,
        #     'server': 'sz-glblic01',
        #     'description': 'Synopls',
        #     'status': 'UP',
        #     'version': '200.1.3'
        # },
        #     {
        #     'index': 2,
        #     'port': 27020,
        #     'server': 'sz-glblic01',
        #     'description': 'Synopls',
        #     'status': 'UP',
        #     'version': '200.1.3'
        # },
        #     {
        #     'index': 2,
        #     'port': 27020,
        #     'server': 'sz-glblic01',
        #     'description': 'Synopls',
        #     'status': 'UP',
        #     'version': '200.1.3'
        # },
        #     {
        #     'index': 2,
        #     'port': 27020,
        #     'server': 'sz-glblic01',
        #     'description': 'Synopls',
        #     'status': 'UP',
        #     'version': '200.1.3'
        # },
        #     {
        #     'index': 2,
        #     'port': 27020,
        #     'server': 'sz-glblic01',
        #     'description': 'Synopls',
        #     'status': 'UP',
        #     'version': '200.1.3'
        # },
        #     {
        #     'index': 2,
        #     'port': 27020,
        #     'server': 'sz-glblic01',
        #     'description': 'Synopls',
        #     'status': 'UP',
        #     'version': '200.1.3'
        # },
        #     {
        #     'index': 2,
        #     'port': 27020,
        #     'server': 'sz-glblic01',
        #     'description': 'Synopls',
        #     'status': 'UP',
        #     'version': '200.1.3'
        # },
        #     {
        #     'index': 2,
        #     'port': 27020,
        #     'server': 'sz-glblic01',
        #     'description': 'Synopls',
        #     'status': 'UP',
        #     'version': '200.1.3'
        # },
        #     {
        #     'index': 2,
        #     'port': 27020,
        #     'server': 'sz-glblic01',
        #     'description': 'Synopls',
        #     'status': 'UP',
        #     'version': '200.1.3'
        # }
    ]
    return render_template('home.html', data=context)


@app.route('/watchedlist')
def setting():

    return render_template('watchedlist.html')
