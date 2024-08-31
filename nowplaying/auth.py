from requests import post
from string import ascii_lowercase,ascii_uppercase,digits
from random import choice
from json import loads, dumps
from base64 import b64encode
global redirect_uri
global CLIENT_ID
global CLIENT_SECRET
with open('config/keys.json', 'r') as f:
	data = loads(f.read())
	CLIENT_ID = data["CLIENT_ID"]
	CLIENT_SECRET = data["CLIENT_SECRET"]
with open('config/config.json', 'r') as f:
	data = loads(f.read())
	redirect_uri = data["redirect_uri"]
def randomword(length):
   letters = ascii_lowercase+ascii_uppercase+digits
   return ''.join(choice(letters) for _ in range(length))

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
	try:
		with open(fr'cache/{user}.json', 'r') as f:
			data = loads(f.read())
			code = data["code"]
	except Exception as e:
		return 404, f"error: user not found\n{e}"
	url= 'https://accounts.spotify.com/api/token'
	form = {
		"code": code,
		"redirect_uri": redirect_uri,
		"grant_type": 'authorization_code'
	}
	headers = {
		'content-type': 'application/x-www-form-urlencoded',
		'Authorization': 'Basic ' + b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')).decode('utf-8')
	}
	try:
		r = post(url, data=form, headers=headers)
	except Exception as e:
		return 500, f"spotify post error\n{e}"
	rjson = r.json()
	try:
		with open(fr'cache/{user}.json', 'w+') as f:
			f.write(dumps(rjson, indent=4))
	except Exception as e:
		return 500, f"error writing to file\n{e}"
	return r.status_code, rjson
def refreshtoken(user):
	global CLIENT_ID
	global CLIENT_SECRET
	try:
		with open(fr'cache/{user}.json', 'r') as f:
			data = loads(f.read())
			refreshToken = data["refresh_token"]
	except Exception as e:
		return 404, f"error: user not found\n{e}"
	form = {
		"grant_type": "refresh_token",
		"refresh_token": refreshToken
	}
	headers= {
		'Content-Type': 'application/x-www-form-urlencoded',
		'Authorization': 'Basic ' + b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')).decode('utf-8')
	}
	url = f"https://accounts.spotify.com/api/token"
	try:
		r = post(url, data=form, headers=headers)
	except Exception as e:
		return 500, f"spotify post error\n{e}"
	rjson = r.json()
	try:
		rjson["refresh_token"]
	except:
		rjson["refresh_token"] = refreshToken
	try:
		with open(fr'cache/{user}.json', 'w+') as f:
			f.write(dumps(rjson, indent=4))
	except Exception as e:
		return 500, f"error writing to file\n{e}"
	return r.status_code, rjson