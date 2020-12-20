import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# Get Spotify username
username = sys.argv[1]
scope = 'playlist-read-private'

# Prompt permissions to user
try:
    token = util.prompt_for_user_token(username, scope=scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope=scope)

# Create spotifyObject
spotifyObject = spotipy.Spotify(auth=token)

# prints readable JSON.
# print(json.dumps(VARIABLE, sort_keys=True, indent=4))

# Store username
user = spotifyObject.current_user()
displayName = user["display_name"]

# Get list of all playlists
# Maxmimum playlist number is 50 for function call
playlists = spotifyObject.current_user_playlists(10, 0)
for playlist in playlists['items']:
    # Check if playlist is created by user.
    if playlist['owner']['display_name'] == displayName:
        # Create a list of tracks
        playlistTracks = spotifyObject.playlist_tracks(playlist['id'], fields=None, limit=100, offset=0, market=None, additional_types=('track',))
        # Loop through all tracks
        for track in playlistTracks['items']:
            # Get year and month track was added to playlist
            trackDate = track['added_at'].split('-')
            trackYear = trackDate[0]
            trackMonth = trackDate[1]
            # Get unique track ID
            trackID = track['track']['album']['artists'][0]['id']

