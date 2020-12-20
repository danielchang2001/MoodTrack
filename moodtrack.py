import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

dict2020 = {
    "01": 0,
    "02": 0,
    "03": 0,
    "04": 0,
    "05": 0,
    "06": 0,
    "07": 0,
    "08": 0,
    "09": 0,
    "10": 0,
    "11": 0,
    "12": 0
}

counter2020 = {
    "01": 0,
    "02": 0,
    "03": 0,
    "04": 0,
    "05": 0,
    "06": 0,
    "07": 0,
    "08": 0,
    "09": 0,
    "10": 0,
    "11": 0,
    "12": 0    
}

# Get Spotify username
username = sys.argv[1]
scope = 'playlist-read-private'
client_id = '81f7cb4b6676434a90522576d7f36b38'
client_secret= '9d44d235ee514940a8d48e9988da6eab'
redirect_uri = 'http://google.com/'

# Prompt permissions to user
try:
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

# Create spotifyObject
spotifyObject = spotipy.Spotify(auth=token)

# prints readable JSON.
# print(json.dumps(VARIABLE, sort_keys=True, indent=4))

# Store username
user = spotifyObject.current_user()
displayName = user["display_name"]

# Get list of all playlists
# Maxmimum playlist number is 50 for function call
playlists = spotifyObject.current_user_playlists(50, 0)
for playlist in playlists['items']:
    # Check if playlist is created by user.
    if playlist['owner']['display_name'] == displayName:
        # Create a list of tracks
        playlistTracks = spotifyObject.playlist_tracks(playlist['id'], fields=None, limit=100, offset=0, market=None, additional_types=('track',))
        # Creates a list of all track IDs from a playlist
        trackIDList = []
        for track in playlistTracks['items']:
            if track['track'] == None:
                continue
            trackIDList.append(track['track']['id'])
        # Loop through all tracks in a playlist
        indexTrackIDList = 0
        audioFeatures = spotifyObject.audio_features(trackIDList)
        for track in playlistTracks['items']:
            # Error check
            if track['track'] == None:
                continue
            if audioFeatures[indexTrackIDList] == None:
                continue
            # Get year and month track was added to playlist
            trackDate = track['added_at'].split('-')
            trackYear = trackDate[0]
            trackMonth = trackDate[1]
            # Increments number of tracks in respective month
            counter2020[trackMonth] = counter2020[trackMonth] + 1
            # Get unique track ID
            trackID = track['track']['id']
            # Get valence of each track
            valence = audioFeatures[indexTrackIDList]['valence']
            if trackYear == '2020':
                dict2020[trackMonth] = dict2020[trackMonth] + valence
            indexTrackIDList += 1
for key in dict2020:
    if counter2020[key] == 0:
        continue
    print(dict2020[key] / counter2020[key])


