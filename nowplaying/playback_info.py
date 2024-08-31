from json import loads
from requests import get
def get_current_playback_info(user):
	try:
		with open(fr'cache/{user}.json', 'r') as f:
			data = loads(f.read())
			access_token = data["access_token"]
			token_type = data["token_type"]
	except Exception as e:
		return 404, f"error: user not found\n{e}"
	url = "https://api.spotify.com/v1/me/player"
	headers = {
		"Authorization": f"{token_type} {access_token}"
	}
	try:
		r = get(url, headers=headers)
	except Exception as e:
		return 500, f"spotify get error\n{e}"
	rjson = r.json()
	progress = int(r[1]["progress_ms"])/1000
	item = rjson["item"]
	name = item["name"]
	duration = int(item["duration_ms"])/1000
	artists = ",".join([artist["name"] for artist in item["artists"]])
	album = item["album"]["name"]
	return (r.status_code, rjson)