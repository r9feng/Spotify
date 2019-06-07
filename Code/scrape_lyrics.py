import numpy as np
import pandas as pd
import re

import lyricsgenius as genius
import os

client_id = 'mVH5TFY8oaj9D0XCP8t1xcqWJT9irp3jrmcSsvZDS0wYNgxCBW8Vp9BoY3_G0OIg'
client_secret = 'WC1seSMHlvKa5_2ZT_qR7TmblZel1WtN1yy61yqriANzN6Tvr2jgalbl-kBdfeCeiKuaXNXhC9XS2edI7DI5Dw'
token = 'U2gZ9KEN7emQrrv9Ee0VoUP4U0wP-MYW0W_w1jiWYWVZub64jLZmElhdw8OWcnqe'
api = genius.Genius(token)

# read in billboard data
billboard = pd.read_csv('Data/billboard.csv')
# read in my favorites data
myPlaylist = pd.read_csv('Data/my_audio.csv')

# retrieve, clean, and write lyrics for billboard songs
def geniusLyrics(song,artist):
    try:
        lyrics_raw = api.search_song(song, artist, get_full_info=False)
        # remove tags like [verse], [chorus], [refrain], etc.
        lyrics_clean = re.sub(r'[\(\[].*?[\)\]]', '', lyrics_raw.lyrics)
        # remove empty lines
        lyrics_clean = os.linesep.join([s for s in lyrics_clean.splitlines() if s])
        return lyrics_clean
    except:
        print('error:' + song + ' ' + artist)
        lyrics_clean = 'error'
        return lyrics_clean

# creating billboard dataset
bb_lyrics = list()
for i in range(len(billboard)): 
    l = geniusLyrics(billboard['song'][i], billboard['artist_base'][i])
    bb_lyrics.append(str(l))

billboard['lyrics'] = bb_lyrics
#billboard = billboard.reset_index()
billboard.tail(5)

# Fixing case-by-case issues
akendrick_lyric = api.search_song('cups', 'anna kendrick', get_full_info=False)
billboard.loc[billboard.song == 'cups (pitch perfect\'s ', 'lyrics'] = akendrick_lyric.lyrics

# creating my favorites dataset
my_lyrics = list()
for i in range(len(myPlaylist)): 
    l = geniusLyrics(myPlaylist['spotify_song'][i], myPlaylist['spotify_artist'][i])
    my_lyrics.append(l)

myPlaylist['lyrics'] = my_lyrics

# write to csv
billboard.to_csv('Data/bb_lyrics.csv', index=None)
myPlaylist.to_csv('Data/my_lyrics.csv', index=None)
