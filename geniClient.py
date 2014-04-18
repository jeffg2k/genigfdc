import os
import requests
import json
import time

BASE_URL = 'https://www.geni.com/'
#REDIRECT_URL = 'http://gfdc.herokuapp.com/home'
REDIRECT_URL = os.getenv('GENI_REDIRECT_URL','http://localhost:5000/home')
AUTH_URL = 'platform/oauth/authorize'
CLIENT_ID = os.getenv('GENI_CLIENT_ID', '')
CLIENT_SECRET = os.getenv('GENI_CLIENT_SECRET', '')
TOKEN_URL = 'https://www.geni.com/platform/oauth/request_token'
PROF_URL = 'https://www.geni.com/api/profile/immediate-family'
IMM_FAM_URL = 'https://www.geni.com/api/?/immediate-family'
#PROF_URL = 'https://www.geni.com/api/profile'
INVALIDATE_URL = 'https://www.geni.com/platform/oauth/invalidate_token'
#PUBLIC_URL = 'http://www.geni.com/people/{name}/{guid}'
PUBLIC_URL = 'http://www.geni.com/people/private/{guid}'
OTHERS_URL = 'https://www.geni.com/api/profile-G{guid}'
GENI_API_COUNT = 0
GENI_API_SLEEP_LIMIT = 50

def buildAuthUrl():
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URL
    }
    params = '&'.join(['%s=%s' % (k, v) for k, v in params.iteritems()])
    url = '%s%s?%s' % (BASE_URL, AUTH_URL, params)
    return url

def getNewToken(code):

    params = {
              'client_id': CLIENT_ID,
              'client_secret': CLIENT_SECRET,
              'code': code,
              'redirect_url': REDIRECT_URL
    }
    tokenResponse = requests.get(TOKEN_URL, params=params)
    tokenResponse = tokenResponse.text
    return tokenResponse

def getProfileDetails(accessToken, profileId):
    payload = {'access_token':accessToken}
    global GENI_API_COUNT
    if GENI_API_COUNT == GENI_API_SLEEP_LIMIT:
        print 'sleeping before geni api calling'
        time.sleep(0.5)
        GENI_API_COUNT = 0
    if not profileId:
        profileResponse = requests.get(PROF_URL, params=payload)
    else:
        url = IMM_FAM_URL.replace('?', profileId)
        profileResponse = requests.get(url, params=payload)
    #print profileResponse.text
    GENI_API_COUNT = GENI_API_COUNT + 1
    profileObj = getProfileObj(profileResponse.text)
    return profileObj

def getOtherProfile(accessToken, guid):
    payload = {'access_token':accessToken}
    url = OTHERS_URL.replace('{guid}', guid)
    profileResponse = requests.get(url, params=payload)
    return profileResponse.text

def getProfileObj(profileResponse):
    data = {}
    jsoncontents = json.loads(profileResponse)
    error = jsoncontents.get('error', False)
    if error != False:
        data['status'] = 'API_ERROR'
        return data
    data['status'] = 'SUCCESS'

    publicUrl = PUBLIC_URL
    #publicUrl = publicUrl.replace('{name}', firstName + '-' + lastName)
    publicUrl = publicUrl.replace('{guid}', jsoncontents['focus']['guid'])
    data['id'] = jsoncontents['focus']['id']
    #data['name'] = firstName + ' ' + lastName
    profileName = jsoncontents['focus'].get('name', '')
    data['profileName'] = profileName
    #data['gender'] = '' #jsoncontents['focus']['gender']
    data['geniLink'] = publicUrl
    data['guid'] = jsoncontents['focus']['guid']
    contents = jsoncontents['nodes']
    relations = []
    for node in contents:
        if node.startswith('profile') and jsoncontents['focus']['id'] != contents[node]['id']:
            #p.addRelation(contents[node]['first_name'] + ' ' + contents[node]['last_name'],
            #          contents[node]['gender'], contents[node]['id'])
            try:
                relations.append({'id':contents[node]['id']})
            except:
                pass
    data['relations'] = relations
    return data

def invalidateToken(accessToken):
    payload = {'access_token':accessToken}
    invResponse = requests.get(INVALIDATE_URL, params=payload)
