import os

def run()
	#search spotify for random songs
	spotify_client = SpotifyClient('a84408bdbc3449deb7c0ac26ab7f60f7')
	random_tracks =spotify_client.get_random_tracks()
	track_ids = [track['id'] for track in random_tracks]

	was_added_to_library = spotify_client.add_tracks_to_library(track_ids)
	if was_added_to_library:
		for track in random_tracks:
			print(f'Added {track['name']} to your library')
if __name__ = '__main__':
	run()