from json import loads
import requests


def get_current_playback_info(user):
	with open(fr'cache/{user}.json', 'r') as f:
		data = loads(f.read())
		access_token = data["access_token"]
		token_type = data["token_type"]
	url = "https://api.spotify.com/v1/me/player"
	headers = {
		"Authorization": f"{token_type} {access_token}"
	}
	r = requests.get(url, headers=headers)
	return (r.status_code, r.json())

r = get_current_playback_info("spotirfy")
progress = int(r[1]["progress_ms"])/1000
item = r[1]["item"]
name = item["name"]
duration = int(item["duration_ms"])/1000
artists = ",".join([artist["name"] for artist in item["artists"]])
album = item["album"]["name"]
print(r[0])
print(name)
print(f"{progress}/{duration}")
print(artists)
print(album)