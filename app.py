import os
from flask import Flask, redirect, request, session, url_for, jsonify, send_file, make_response, Response
import requests
from datetime import datetime, timedelta
import json
import requests
from geniClient import buildAuthUrl, getNewToken, invalidateToken, getProfileDetails, getImmFamilyDetails
from profiles import Relation, Profile

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
    return send_file('templates/index.html')

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
    profileId = request.args.get('profileId')
    print 'profileId:' + str(profileId)
    if not accessToken:
        redirect(url_for('login'))
    #Load from session if already there.
    try:
        if session[profileId] != None:
            profileData = session[profileId]
            print 'loaded from session================'
            return jsonify(profileData)
    except KeyError:
        pass

    profileData = getProfileDetails(accessToken, profileId)
    print 'got profileObj'
    print profileData['id']
    if profileData != None:
        print 'inside if'
        session[profileData['id']] = profileData
        print 'session obj set'
        print session[profileData['id']]
    print 'returning json'
    print profileData
    return jsonify(profileData)

"""@app.route('/getImmFamily', methods=['GET'])
def getImmFamily():
    print 'in /getImmFamily'
    profileId = request.args.get('profileId')
    accessToken = session['accessToken']
    if not accessToken:
        redirect(url_for('login'))
    try:
        if session[profileId] != None:
            profileData = session[profileId]
            print 'loaded from session================'
            return jsonify(profileData)
    except KeyError:
        pass
    profileData = getImmFamilyDetails(accessToken, profileId)
    if profileData != None:
        session[profileData['id']] = profileData
    return jsonify(profileData)"""

@app.route('/logout')
def logout():
    accessToken = session['accessToken']
    invalidateToken(accessToken)
    session.clear()
    return send_file('templates/login.html')

@app.errorhandler(500)
def page_not_found(error):
    print error
    return 'This page does not exist', 500

@app.route('/getJsonTest', methods=['GET'])
def getJsonTest():
    geniFile = open('./geni.json','r')
    contents = geniFile.read()
    jsoncontents = json.loads(contents)
    p = Profile(jsoncontents['focus']['id'], 'publicUrl',
            'firstName' + ' ' + 'lastName', [], jsoncontents['focus']['gender'])
    contents = jsoncontents['nodes']
    for node in contents:
        if node.startswith('profile') and jsoncontents['focus']['id'] != contents[node]['id']:
            p.addRelation(contents[node]['first_name'] + ' ' + contents[node]['last_name'],
                      contents[node]['gender'], contents[node]['id'])
    data = {}
    data['id'] = p.id
    data['name'] = p.name
    data['gender'] = p.gender
    data['geniLink'] = p.geniLink
    relations = []
    for node in p.relations:
        relations.append({'id':node.id,'name':node.name,'gender':node.gender})
    data['relations'] = relations
    print data
    return jsonify(data)

app.secret_key = '12345abcde'

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = False
    #app.testing = True
    app.secret_key = '12345abcde'
    app.run(host='localhost', port=port)
