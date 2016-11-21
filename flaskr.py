import os
import uuid
from ConfigParser import ConfigParser
from flask import (flash, Flask, redirect, render_template, url_for)


"""
COnfiguration check
"""
env_files = ['flaskr.ini', ]
for file in env_files:
    if not os.path.isfile(file):
        raise IOError('Generate env files before running the application.')


"""
Environment settings.
"""
config = ConfigParser()
config.read('flaskr.ini')


"""
Application settings.
"""

# My personal account (limited)
custom_config = {
    'SESSION_TYPE': 'filesystem',
    'EXAMPLE2_KEY': {}
}

app = Flask(__name__)
app.secret_key = uuid.uuid1()
app.config.update(custom_config)


"""
Views
"""


@app.route('/testing_site', methods=['GET', 'POST'])
def testing_site():
    flash('This is a testing site.')
    posts = []
    return render_template('show_posts.html', posts=posts)


@app.route('/')
def index():
    return redirect(url_for('testing_site'))


@app.route('/invalid_request')
def invalid_request():
    flash('Request invalid.')
    return render_template('show_posts.html')


if __name__ == '__main__':
    app.run()
