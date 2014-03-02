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
    tokenResponse = requests.get(TOKEN_URL, params=params)
    tokenResponse = tokenResponse.text
    print 'got access tokens'
    return tokenResponse

def getProfileDetails(accessToken, profileId):
    payload = {'access_token':accessToken}
    if not profileId:
        profileResponse = requests.get(PROF_URL, params=payload)
    else:
        url = IMM_FAM_URL.replace('?', profileId)
        profileResponse = requests.get(url, params=payload)
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
    #p = Profile(jsoncontents['focus']['id'], publicUrl,
    #        firstName + ' ' + lastName, [], jsoncontents['focus']['gender'])
    data = {}
    data['id'] = jsoncontents['focus']['id']
    data['name'] = firstName + ' ' + lastName
    data['gender'] = jsoncontents['focus']['gender']
    data['geniLink'] = publicUrl
    contents = jsoncontents['nodes']
    relations = []
    for node in contents:
        if node.startswith('profile') and jsoncontents['focus']['id'] != contents[node]['id']:
            #p.addRelation(contents[node]['first_name'] + ' ' + contents[node]['last_name'],
            #          contents[node]['gender'], contents[node]['id'])
            try:
                relations.append({'id':contents[node]['id'],
                              'name':contents[node]['first_name'] + ' ' + contents[node]['last_name'],
                              'gender':contents[node]['gender']})
            except:
                pass
    data['relations'] = relations
    return data

def invalidateToken(accessToken):
    payload = {'access_token':accessToken}
    invResponse = requests.get(INVALIDATE_URL, params=payload)
    print invResponse.text
