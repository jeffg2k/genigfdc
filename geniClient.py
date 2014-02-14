import requests
import json
from profiles import Relation, Profile

BASE_URL = 'https://www.geni.com/'
REDIRECT_URL = 'http://mysterious-citadel-7993.herokuapp.com/home'
#REDIRECT_URL = 'http://localhost:5000/home'
AUTH_URL = 'platform/oauth/authorize'
CLIENT_ID = '0FxhNjhtYXRPKRqDBOCJgJOhukrg1xIACIZr0LZO'
CLIENT_SECRET = '0t72HNiBHuNCGhnD2Y7a9zu65lJaomls4UPXJCe0'
TOKEN_URL = 'https://www.geni.com/platform/oauth/request_token'
PROF_URL = 'https://www.geni.com/api/profile/immediate-family'
IMM_FAM_URL = 'https://www.geni.com/api/?/immediate-family'
#PROF_URL = 'https://www.geni.com/api/profile'
INVALIDATE_URL = 'https://www.geni.com/platform/oauth/invalidate_token'
PUBLIC_URL = 'http://www.geni.com/people/{name}/{guid}'

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
    print 'calling request token api'
    tokenResponse = requests.get(TOKEN_URL, params=params)
    print 'called request token api'
    #print tokenResponse.text
    tokenResponse = tokenResponse.text
    print 'sending response'
    return tokenResponse

def getProfileDetails(accessToken):
    payload = {'access_token':accessToken}
    profileResponse = requests.get(PROF_URL, params=payload)
    profileObj = getProfileObj(profileResponse.text)
    return profileObj

def getImmFamilyDetails(accessToken, profileId):
    payload = {'access_token':accessToken}
    url = IMM_FAM_URL.replace('?', profileId)
    profileResponse = requests.get(url, params=payload)
    profileObj = getProfileObj(profileResponse.text)
    return profileObj

def getProfileObj(profileResponse):
    jsoncontents = json.loads(profileResponse)
    firstName = jsoncontents['focus']['first_name']
    lastName = jsoncontents['focus']['last_name']
    publicUrl = PUBLIC_URL
    publicUrl = publicUrl.replace('{name}', firstName + '-' + lastName)
    publicUrl = publicUrl.replace('{guid}', jsoncontents['focus']['guid'])
    p = Profile(jsoncontents['focus']['id'], publicUrl,
            firstName + ' ' + lastName, [], jsoncontents['focus']['gender'])
    contents = jsoncontents['nodes']
    for node in contents:
        if node.startswith('profile') and jsoncontents['focus']['id'] != contents[node]['id']:
            p.addRelation(contents[node]['first_name'] + ' ' + contents[node]['last_name'],
                      contents[node]['gender'], contents[node]['id'])

    return p

def invalidateToken(accessToken):
    payload = {'access_token':accessToken}
    invResponse = requests.get(INVALIDATE_URL, params=payload)
    print invResponse.text
