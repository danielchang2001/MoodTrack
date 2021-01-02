import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
import numpy as np
import time
from json.decoder import JSONDecodeError
from matplotlib import pyplot as plt

# valence20XX: summed valence value for each month
# counter20XX: number of tracks for each month (used to calculate avg. valence for each month)
valence2020 = {
    "01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0, "12": 0
}
counter2020 = {
    "01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0, "12": 0
}
valence2019 = {
    "01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0, "12": 0
}
counter2019 = {
    "01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0, "12": 0
}
valence2018 = {
    "01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0, "12": 0
}
counter2018 = {
    "01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0, "12": 0
}
valence2017 = {
    "01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0, "12": 0
}
counter2017 = {
    "01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0, "12": 0
}
valence2016 = {
    "01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0, "12": 0
}
counter2016 = {
    "01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0, "12": 0
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
# Maximum playlist number is 50 for function call, so loop after 50
offset = 0
while offset <= 300:
    playlists = spotifyObject.current_user_playlists(50, offset)
    for playlist in playlists['items']:
        # Check if playlist is created by user.
        if playlist['owner']['display_name'] == displayName:
            # Create a list of tracks
            playlistTracks = spotifyObject.playlist_tracks(playlist['id'], fields=None, limit=100, offset=0, market=None, additional_types=('track',))
            trackIDList = np.array([])
            for track in playlistTracks['items']:
                # Error check
                if (track['track'] == None) or (track['track']['id'] == None):
                    continue
                # Creates a single element list for the track ID. (func audio_features requires a list for input)
                trackIDList = np.append(trackIDList, track['track']['id'])
            audioFeatures = spotifyObject.audio_features(trackIDList)
            trackIDIndex = 0
            # Loop through all tracks in a playlist
            for track in playlistTracks['items']:
                # Error check
                if (track['track'] == None) or (track['track']['id'] == None) or (audioFeatures[trackIDIndex]) == None:
                    continue
                # Get valence of each track
                valence = audioFeatures[trackIDIndex]['valence']
                # Get year and month track was added to playlist
                trackDate = track['added_at'][:7].split('-') # Truncated date to only year and month for efficiency.
                trackYear = trackDate[0]
                trackMonth = trackDate[1]
                # Increments number of tracks in respective month
                # Get unique track ID
                trackID = track['track']['id']
                # If track was added to playlist in 2020:
                if trackYear == '2020':
                    valence2020[trackMonth] = valence2020[trackMonth] + valence
                    counter2020[trackMonth] = counter2020[trackMonth] + 1
                    trackIDIndex += 1
                    continue
                # 2019
                if trackYear == '2019':
                    valence2019[trackMonth] = valence2019[trackMonth] + valence
                    counter2019[trackMonth] = counter2019[trackMonth] + 1
                    trackIDIndex += 1
                    continue
                # 2018
                if trackYear == '2018':
                    valence2018[trackMonth] = valence2018[trackMonth] + valence
                    counter2018[trackMonth] = counter2018[trackMonth] + 1
                    trackIDIndex += 1
                    continue
                # 2017
                if trackYear == '2017':
                    valence2017[trackMonth] = valence2017[trackMonth] + valence
                    counter2017[trackMonth] = counter2017[trackMonth] + 1
                    trackIDIndex += 1
                    continue
                # 2016
                if trackYear == '2016':
                    valence2016[trackMonth] = valence2016[trackMonth] + valence
                    counter2016[trackMonth] = counter2016[trackMonth] + 1
                    trackIDIndex += 1
                    continue
                trackIDIndex += 1
    offset += 50

xMonths = np.array([1,2,3,4,5,6,7,8,9,10,11,12])
y2020 = np.array([])
y2019 = np.array([])
y2018 = np.array([])
y2017 = np.array([])
y2016 = np.array([])

x_indexes = np.arange(1, 13)

for key in valence2020:
    if counter2020[key] == 0:
        y2020 = np.append(y2020, None)
        continue
    y2020 = np.append(y2020, (valence2020[key] / counter2020[key]))

plt.plot(xMonths, y2020, color="#003f5c", label='2020')

for key in valence2019:
    if counter2019[key] == 0:
        y2019 = np.append(y2019, None)
        continue
    y2019 = np.append(y2019, (valence2019[key] / counter2019[key]))

plt.plot(xMonths, y2019, color="#58508d", label='2019')

for key in valence2018:
    if counter2018[key] == 0:
        y2018 = np.append(y2018, None)
        continue
    y2018 = np.append(y2018, (valence2018[key] / counter2018[key]))

plt.plot(xMonths, y2018, color="#bc5090", label='2018')

for key in valence2019:
    if counter2017[key] == 0:
        y2017 = np.append(y2017, None)
        continue
    y2017 = np.append(y2017, (valence2017[key] / counter2017[key]))

plt.plot(xMonths, y2017, color="#ff6361", label='2017')

for key in valence2016:
    if counter2016[key] == 0:
        y2016 = np.append(y2016, None)
        continue
    y2016 = np.append(y2016, (valence2016[key] / counter2016[key]))

plt.plot(xMonths, y2016, color="#ffa600", label='2016')

plt.xlabel('Months')
plt.ylabel('Avg. Music Happiness (0-1)')
plt.title('Avg. Music Happiness (0-1) by Months')
plt.xticks(x_indexes)
plt.legend()

plt.show()


