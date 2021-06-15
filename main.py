import requests
import json

BASE_URL = "https://tunefind.com/api/frontend"
SEASON = "/show/black-lightning/season/{idx}?fields=episodes"
EPISODE = "/episode/{idx}?fields=song-events"


def get_season_count():
	resp = requests.get(BASE_URL + "/show/black-lightning?fields=seasons&metatags=1")
	if resp.status_code == 404:
		# RIP
		return

	resp = resp.json()
	return len(resp['seasons'])


def get_episode_ids_for_season(season: int):
	resp = requests.get(BASE_URL + SEASON.format(idx=season))
	if resp.status_code == 404:
		# RIP
		return

	resp = resp.json()
	return [r['id'] for r in resp['episodes']]


def get_songs(idx: int):
	resp = requests.get(BASE_URL + EPISODE.format(idx=str(idx)))
	if resp.status_code == 404:
		return

	resp = resp.json()['episode']
	r = {}
	for song in resp['song_events']:
		song = song['song']
		r[song['name']] = {"album": song['album'], "artists": [a['name'] for a in song['artists']]}
	return r
	

def generate():
	count = get_season_count()
	j = {}
	for idx in range(count):
		idx = idx + 1
		episodes = get_episode_ids_for_season(idx)
		j[idx] = [get_songs(r) for r in episodes]

	with open("data.json", "w") as fp:
		json.dump(j, fp)


if __name__ == "__main__":
	generate()
