import os
from flask import Flask, redirect, request, session, url_for, jsonify, send_file, make_response
import requests
from datetime import datetime, timedelta
import json
import requests
from geniClient import buildAuthUrl, getNewToken, invalidateToken, getFamilyDetails

app = Flask(__name__)

@app.route('/')
def index():
    print 'in /'
    return send_file('templates/login.html')

@app.route('/login')
def login():
    return redirect(buildAuthUrl())

@app.route('/home')
def home():
    print 'in /home'
    code = request.args.get('code')
    print 'code-' + code
    print 'expires-' + request.args.get('expires_in')
    tokenResponse = getNewToken(code)
    print tokenResponse
    setTokens(tokenResponse)
    return send_file('templates/home.html')

def setTokens(tokenResponse):
    tokenResponse = json.loads(tokenResponse)
    session['accessToken'] = tokenResponse['access_token']
    session['refreshToken'] = tokenResponse['refresh_token']
    session['tokenExpiration'] = tokenResponse['expires_in']
    print session['accessToken']
    print session['refreshToken']


@app.route('/getProfile', methods=['GET'])
def getProfile():
    print 'in /getProfile'
    accessToken = session['accessToken']
    if not accessToken:
        redirect(url_for('login'))
    profileResponse = getFamilyDetails(accessToken)
    print profileResponse
    return profileResponse

@app.route('/logout')
def logout():
    accessToken = session['accessToken']
    invalidateToken(accessToken)
    session.clear()
    return send_file('templates/login.html')

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = False
    app.secret_key = '12345abcde'
    app.run(host='localhost', port=port)