import os
from flask import Flask, redirect, request, session, url_for, jsonify, send_file, make_response, render_template
import requests
from datetime import datetime, timedelta
import json
import requests

app = Flask(__name__)

BASE_URL = 'https://www.geni.com/'
REDIRECT_URL = 'http://mysterious-citadel-7993.herokuapp.com/home'
#REDIRECT_URL = 'http://localhost:5000/home'

@app.route('/')
def index():
    print 'in /'
    return send_file('templates/login.html')

@app.route('/login')
def login():
    params = {
        'client_id': '0FxhNjhtYXRPKRqDBOCJgJOhukrg1xIACIZr0LZO',
        'redirect_uri': REDIRECT_URL
    }
    return redirect(buildAuthUrl('platform/oauth/authorize', params=params))

def buildAuthUrl(endpoint, params=''):
    if params != '':
        params = '&'.join(['%s=%s' % (k, v) for k, v in params.iteritems()])
    url = '%s%s?%s' % (BASE_URL, endpoint, params)
    return url

@app.route('/home')
def home():
    print 'in /home'
    code = request.args.get('code')
    print 'code-' + code
    print 'expires-' + request.args.get('expires_in')
    tokenResponse = getNewTokenFromApi(code)
    print 'got token!!!!'
    print tokenResponse
    tokenResponse = json.loads(tokenResponse)
    print 'got token loaded setting in session'
    print tokenResponse
    print tokenResponse['access_token']
    session['accessToken'] = tokenResponse['access_token']
    print 'session accesstoken'
    session['refreshToken'] = tokenResponse['refresh_token']
    print 'session refreshtoken'
    session['tokenExpiration'] = tokenResponse['expires_in']
    print 'sending home html'
    return send_file('templates/home.html')

@app.route('/getProfile', methods=['GET'])
def getProfile():
    print 'in /getProfile'
    #profileId = request.args.get('profileId')
    #record = json.loads(request.data)
    FAM_URL = 'https://www.geni.com/api/profile/immediate-family'
    PROF_URL = 'https://www.geni.com/api/profile'
    #print profileId
    #profileResponse = requests.get(PROFILE_URL);//6000000024491145741
    accessToken = session['accessToken']
    payload = {'access_token':accessToken}
    profileResponse = requests.get(FAM_URL, params=payload)
    print profileResponse.text
    return profileResponse.text

@app.route('/logout')
def logout():
    accessToken = session['accessToken']
    payload = {'access_token':accessToken}
    INVALIDATE_URL = 'https://www.geni.com/platform/oauth/invalidate_token'
    invResponse = requests.get(INVALIDATE_URL, params=payload)
    print invResponse.text
    session.clear()
    return send_file('templates/login.html')

def getNewTokenFromApi(code):
    url = 'https://www.geni.com/platform/oauth/request_token'
    params = {
              'client_id': '0FxhNjhtYXRPKRqDBOCJgJOhukrg1xIACIZr0LZO',
              'client_secret': '0t72HNiBHuNCGhnD2Y7a9zu65lJaomls4UPXJCe0',
              'code': code,
              'redirect_url': REDIRECT_URL
    }
    print 'calling request token api'
    tokenResponse = requests.get(url, params=params)
    print 'called request token api'
    print tokenResponse.text
    tokenResponse = tokenResponse.text
    print 'sending response'
    return tokenResponse

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.secret_key = '12345567890'
    app.run(host='localhost', port=port)