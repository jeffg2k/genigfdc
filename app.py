import os
from flask import Flask, redirect, request, session, url_for, jsonify, send_file, make_response, render_template
import requests
from datetime import datetime, timedelta
import json
import requests

app = Flask(__name__)

BASE_URL = 'https://www.geni.com/'

@app.route('/')
def index():
    print 'in /'
    #return 'Hello from GeniApp!'
    #if(isTokenExpired()):
    #    return send_file('templates/login.html')
    #else:
    #    return send_file('templates/home.html')
    return send_file('templates/login.html')

@app.route('/login')
def login():
    params = {
        'client_id': '0FxhNjhtYXRPKRqDBOCJgJOhukrg1xIACIZr0LZO',
        'redirect_uri': 'http://mysterious-citadel-7993.herokuapp.com/home'
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
    #oauthResponse = getToken(code=request.args.get('code'))
    jsonToken = getToken(code)
    print 'got token!!!!'
    print jsonToken
    return send_file('templates/home.html')

@app.route('/getProfile', methods=['GET'])
def getProfile():
    print 'in /getProfile'
    profileId = request.args.get('profileId')
    #record = json.loads(request.data)
    FAM_URL = 'https://www.geni.com/api/profile/immediate-family'
    PROF_URL = 'https://www.geni.com/api/profile'
    print profileId
    #profileResponse = requests.get(PROFILE_URL);//34655101643
    payload = {'ids': profileId, 'access_token':'5e4qSBXxtEctU3JTuY3tJjAZx4sCxRyKLzKnOLSe'}
    profileResponse = requests.get(FAM_URL, params=payload)
    print profileResponse.text
    return profileResponse.text

def isTokenExpired():
    if os.path.exists('./auth-keys'):
        boxFile = open('./auth-keys', 'r')
        tokenResponse = {}
        tokenResponse['access_token'] = boxFile.readline().rstrip()
        tokenResponse['refresh_token'] = boxFile.readline().rstrip()
        tokenResponse['expires_in'] = boxFile.readline().rstrip()
        boxFile.close()
        oauthExpirationStr = tokenResponse['expires_in'][:19]
        oauthExpirationDate = datetime.strptime(oauthExpirationStr, '%Y-%m-%d %H:%M:%S')
        print 'oauthExpirationDate-' + oauthExpirationDate.__str__()
        currentTime = datetime.now()
        delta = currentTime - oauthExpirationDate
        if(delta.total_seconds() > 0):
            getRefreshTokenFromApi(tokenResponse['refresh_token'])
        return False
    return True

def getToken(code):
    print 'in getToken'
    if os.path.exists('./auth-keys'):
        boxFile = open('./auth-keys', 'r')
        tokenResponse = {}
        tokenResponse['access_token'] = boxFile.readline().rstrip()
        tokenResponse['refresh_token'] = boxFile.readline().rstrip()
        tokenResponse['expires_in'] = boxFile.readline().rstrip()
        boxFile.close()
        print 'expires_in' + tokenResponse['expires_in']
        oauthExpirationStr = tokenResponse['expires_in'][:19]
        print 'oauthExpirationStr' + oauthExpirationStr
        #Format 2013-11-30 03:36:23#
        oauthExpirationDate = datetime.strptime(oauthExpirationStr, '%Y-%m-%d %H:%M:%S')
        print 'oauthExpirationDate-' + oauthExpirationDate.__str__()
        currentTime = datetime.now()
        delta = currentTime - oauthExpirationDate
        if(delta.total_seconds() > 0):
            print 'token expired'
            tokenResponse = getRefreshTokenFromApi(tokenResponse['refresh_token'])
    else:
        tokenResponse = getNewTokenFromApi(code)
    return tokenResponse

def getNewTokenFromApi(code):
    url = 'https://www.geni.com/platform/oauth/request_token'
    params = {
              'client_id': '0FxhNjhtYXRPKRqDBOCJgJOhukrg1xIACIZr0LZO',
              'client_secret': '0t72HNiBHuNCGhnD2Y7a9zu65lJaomls4UPXJCe0',
              'code': code,
              'redirect_url': 'http://mysterious-citadel-7993.herokuapp.com/home'
    }
    print 'calling request token api'
    tokenResponse = requests.get(url, params=params)
    print 'called request token api'
    print tokenResponse.text
    #tokenResponse = json.dumps(tokenResponse.text)
    #tokenResponse = json.loads(tokenResponse)
    tokenResponse = tokenResponse.json
    #tokenResponse = tokenResponse.json()
    accessToken = tokenResponse['access_token']
    refreshToken = tokenResponse['refresh_token']
    tokenExpiration = tokenResponse['expires_in']
    oauthExpiration= (datetime.now()
                      + timedelta(seconds=tokenExpiration - 15))
    boxFile = open('./auth-keys', 'w')
    boxFile.write(accessToken + '\n')
    boxFile.write(refreshToken + '\n')
    boxFile.write(str(oauthExpiration))
    boxFile.flush()
    boxFile.close()
    return tokenResponse

def getRefreshTokenFromApi(refreshToken):
    url = 'https://www.geni.com/platform/oauth/request_token'
    params = {
              'client_id': '0FxhNjhtYXRPKRqDBOCJgJOhukrg1xIACIZr0LZO',
              'client_secret': '0t72HNiBHuNCGhnD2Y7a9zu65lJaomls4UPXJCe0',
              'redirect_url': 'http://mysterious-citadel-7993.herokuapp.com/home',
              'refresh_token': refreshToken,
              'grant_type': 'refresh_token'
    }
    print 'calling refresh token api'
    tokenResponse = requests.get(url, params=params)
    print 'called refresh token api'
    print tokenResponse.text
    tokenResponse = tokenResponse.json
    accessToken = tokenResponse.get('access_token')
    refreshToken = tokenResponse.get('refresh_token')
    tokenExpiration = tokenResponse.get('expires_in')
    oauthExpiration= (datetime.now()
                      + timedelta(seconds=tokenExpiration - 15))
    boxFile = open('./auth-keys', 'w')
    boxFile.write(accessToken + '\n')
    boxFile.write(refreshToken + '\n')
    boxFile.write(str(oauthExpiration))
    boxFile.flush()
    boxFile.close()
    return tokenResponse

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = False
    app.secret_key = '12345567890'
    app.run(host='localhost', port=port)