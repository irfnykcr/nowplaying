import flask
from json import loads, dumps
import os
app = flask.Flask(__name__)

@app.route('/callback')
def callback():
	args = flask.request.args
	code = args.get('code')
	state = args.get('state')
	if os.path.exists("cache/spotirfy.json"):
		with open('cache/spotirfy.json', 'r') as f:
			_f = f.read()
			if len(_f) > 0 and type(eval(_f)) == dict:
				print("2222")
				data = loads(dumps(f.read()))
			else:
				data = loads(dumps({}))
			print("d:",data)
		with open('cache/spotirfy.json', 'w') as f:
			data["code"] = code
			data["state"] = state
			data = dumps(data, indent=4)
			print("d:", data)
			f.write(data)
	else:
		with open('cache/spotirfy.json', 'w+') as f:
			f.write(f'{{"code": "{code}", "state": "{state}"}}')
	return "ok"
app.run(port=8000, debug=True)