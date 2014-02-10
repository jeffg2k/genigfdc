import requests

BASE_URL = 'https://www.geni.com/'
#REDIRECT_URL = 'http://mysterious-citadel-7993.herokuapp.com/home'
REDIRECT_URL = 'http://localhost:5000/home'
AUTH_URL = 'platform/oauth/authorize'
CLIENT_ID = '0FxhNjhtYXRPKRqDBOCJgJOhukrg1xIACIZr0LZO'
CLIENT_SECRET = '0t72HNiBHuNCGhnD2Y7a9zu65lJaomls4UPXJCe0'
TOKEN_URL = 'https://www.geni.com/platform/oauth/request_token'
FAM_URL = 'https://www.geni.com/api/profile/immediate-family'
PROF_URL = 'https://www.geni.com/api/profile'
INVALIDATE_URL = 'https://www.geni.com/platform/oauth/invalidate_token'

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
    print tokenResponse.text
    tokenResponse = tokenResponse.text
    print 'sending response'
    return tokenResponse

def getFamilyDetails(accessToken):
    payload = {'access_token':accessToken}
    profileResponse = requests.get(FAM_URL, params=payload)
    print profileResponse.text
    return profileResponse.text

def invalidateToken(accessToken):
    payload = {'access_token':accessToken}
    invResponse = requests.get(INVALIDATE_URL, params=payload)
    print invResponse.text
