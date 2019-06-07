import numpy as np
import pandas as pd

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid ="b415f63717d6452cba50686d414a090a"
secret = "8af14e75f51549ed8c6a44435088366f"

token = SpotifyClientCredentials(client_id=cid, client_secret=secret)
cache_token = token.get_access_token()
spotify = spotipy.Spotify(cache_token)
sp = spotipy.Spotify(auth=cache_token)

# read billboard data
billboard = pd.read_csv('Data/billboard.csv')

def spotifyFeatures(songs_df):
    """
    Function queries the spotifyAPI, by using the artist name and the song title
    """
    # search for track + name
    audio_features_df = pd.DataFrame()

    failed = []
    for index, row in songs_df.iterrows():
        name = row['song']
        artist = row['artist_base']
        year = row['year']
        try:
            results = sp.search(q=name + ' ' + artist, type='track',limit=1)
            uri = results['tracks']['items'][0]['uri']
            sp_song = results['tracks']['items'][0]['name']
            sp_artist = results['tracks']['items'][0]['artists'][0]['name']
            album = results['tracks']['items'][0]['album']['name']
            popularity = results['tracks']['items'][0]['popularity']
            release_date = results['tracks']['items'][0]['album']['release_date']

            audio_feat = sp.audio_features(uri)
            af = audio_feat[0]
            af.pop('analysis_url')
            af.pop('track_href')
            af['spotify_song'] = sp_song
            af['spotify_album'] = album
            af['spotify_artist'] = sp_artist
            af['billboard_name'] = name
            af['billboard_artist'] = artist
            af['popularity'] = popularity
            af['release_date'] = release_date
            af['bb_index'] = index

            audio_features_df = audio_features_df.append(af, ignore_index=True)
        except:
            print('failed song {}: {} by {}'.format(index, name, artist, year))
            failed.append([name, artist, year])
    failed = pd.DataFrame(failed, columns=['song', 'artist', 'year'])
    return audio_features_df, failed

# create billboard audio features dataset
audio, fails = spotifyFeatures(billboard)

# retrieving my music
user_id = 'spotify:user:rfeng888'
playlist_id = 'spotify:user:rfeng888:playlist:0rIB83Lwqpfmg5QqDMeRdz'

project_pl = sp.user_playlist_tracks(user_id, playlist_id, fields='items,uri,name,id,total')

def playlistFeatures(playlist):
    """
    Function retreives audio features from a specified Spotify playlist track listing
    """
    playlist_df = pd.DataFrame()

    pl = playlist['items']
    for t in range(len(pl)):
        try:
            uri = pl[t]['track']['uri']
            sp_song = pl[t]['track']['name']
            sp_artist = pl[t]['track']['artists'][0]['name']
            album = pl[t]['track']['album']['name']
            popularity = pl[t]['track']['popularity']
            release_date = pl[t]['track']['album']['release_date']

            audio_feat = sp.audio_features(uri)
            af = audio_feat[0]
            af.pop('analysis_url')
            af.pop('track_href')
            af['spotify_song'] = sp_song
            af['spotify_album'] = album
            af['spotify_artist'] = sp_artist
            af['popularity'] = popularity
            af['release_date'] = release_date

            playlist_df = playlist_df.append(af, ignore_index=True)
        except:
            print('error')
    return playlist_df

pl_df = playlistFeatures(project_pl)

# removing entirely foreign language and missing songs
audio_clean = audio[audio.id != '2t2rwus7ggTrrj9kpA1K2e']
audio_clean = audio_clean[audio_clean.id != '157B3Zj5gt4JMMlglTXCDt']
audio_clean = audio_clean[audio_clean.id != '6VQ1iGUwAyFugBI73h1iqs']

# write to csv
audio_clean.to_csv('Data/bb_audio.csv', index=None)
pl_df.to_csv('Data/my_audio.csv', index=None)