from mongoengine import connect
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from nemo_demoer_mongodb_client import NemoDemoerMongoDBClient
import validators
from creds import admin

application = Flask(__name__)
auth = HTTPBasicAuth()
connect(db='nemo_auth')

nemo_demoer_client = NemoDemoerMongoDBClient()

@auth.get_password
def get_pw(username):
    if username in admin:
        return admin.get(username)
    return None

@application.route('/')
def test_online():
    return jsonify({'status': 'online'})

@application.route('/admin/enroll/', methods=['GET', 'POST'])
@auth.login_required
def enroll_demo_user():
    error = None
    response = None
    if request.method == 'POST':
        user_id = request.form['username']
        password = request.form['password']
        household_id = request.form['household_id']
        container_url = request.form['container_url']
        res = nemo_demoer_client.enroll_demoer(user_id, password, household_id, container_url)
        if isinstance(res, dict):
            response = res
        else:
            error = res
    return render_template('enroll.html', error=error, response=response)

@application.route('/admin/delete/', methods=['GET', 'POST'])
@auth.login_required
def delete_demo_user():
    error = None
    response = None
    if request.method == 'POST':
        user_id = request.form['username']
        res = nemo_demoer_client.delete_demoer(user_id)
        if isinstance(res, dict):
            response = res
        else:
            error = res
    return render_template('delete.html', error=error, response=response)

@application.route('/login/', methods=['GET', 'POST'])
def demoer_login():
    error = None
    if request.method == 'POST':
        user_id = request.form['username']
        password = request.form['password']
        response = nemo_demoer_client.demoer_login(user_id, password)
        if validators.url(response) == True:
            return redirect(response)
        else:
            error = response
    return render_template('login.html', error=error)

if __name__ == "__main__":
    application.debug = True
    application.run(host='0.0.0.0')