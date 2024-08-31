import requests
import random, string
from json import loads, dumps
import base64


global redirect_uri
global CLIENT_ID
global CLIENT_SECRET
with open('config/keys.json', 'r') as f:
	data = loads(f.read())
	CLIENT_ID = data["CLIENT_ID"]
	CLIENT_SECRET = data["CLIENT_SECRET"]
redirect_uri = 'http://localhost:8000/callback'

def randomword(length):
   letters = string.ascii_lowercase+string.ascii_uppercase+string.digits
   return ''.join(random.choice(letters) for i in range(length))

def getauthurl():
	global redirect_uri
	global CLIENT_ID
	response_type = 'code'
	scope = 'user-modify-playback-state user-read-currently-playing user-read-playback-state'
	state = randomword(16)
	url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type={response_type}&redirect_uri={redirect_uri}&scope={scope}&state={state}"
	return url

def getaccesstoken(user):
	global redirect_uri
	global CLIENT_ID
	global CLIENT_SECRET
	with open(fr'cache/{user}.json', 'r') as f:
		data = loads(f.read())
		code = data["code"]
	url= 'https://accounts.spotify.com/api/token'
	form = {
		"code": code,
		"redirect_uri": redirect_uri,
		"grant_type": 'authorization_code'
	}
	headers = {
		'content-type': 'application/x-www-form-urlencoded',
		'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')).decode('utf-8')
	}
	r = requests.post(url, data=form, headers=headers)
	rjson = r.json()
	print("status:", r.status_code)
	with open(fr'cache/{user}.json', 'w+') as f:
		f.write(dumps(rjson, indent=4))
	return r.status_code, rjson
def refreshtoken(user):
	global CLIENT_ID
	global CLIENT_SECRET
	with open(fr'cache/{user}.json', 'r') as f:
		data = loads(f.read())
		refreshToken = data["refresh_token"]
	form = {
		"grant_type": "refresh_token",
		"refresh_token": refreshToken
	}
	headers= {
		'Content-Type': 'application/x-www-form-urlencoded',
		'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')).decode('utf-8')
	}
	url = f"https://accounts.spotify.com/api/token"
	r = requests.post(url, data=form, headers=headers)
	rjson = r.json()
	print("status:", r.status_code)
	try:
		rjson["refresh_token"]
	except:
		rjson["refresh_token"] = refreshToken
	with open(fr'cache/{user}.json', 'w+') as f:
		f.write(dumps(rjson, indent=4))
	return r.status_code, rjson
	
# print(getauthurl())
print(getaccesstoken('spotirfy'))
# print(refreshtoken('spotirfy'))