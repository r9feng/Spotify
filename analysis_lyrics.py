import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# import data
bb = pd.read_csv('Data/bbMaster.csv')
my = pd.read_csv('Data/myMaster.csv')
master = pd.read_csv('Data/master.csv')
len(master.columns)

# generate word clouds
bb_words = ''.join(bb.lyrics)
my_words = ''.join(my.lyrics)
bb_wcloud = WordCloud(width=1000, height=500, collocations = False).generate(bb_words.lower())
my_wcloud = WordCloud(width=1000, height=500, collocations = False).generate(my_words.lower())

bb_wcloud.to_file('Images/WordClouds/all_bbWC' + ".png")
my_wcloud.to_file('Images/WordClouds/all_myWC' + ".png")

# plots of lyrical features
plt.figure(1, figsize=(20, 10),)

hfont = {'fontname':'Proxima Nova'}



lyric_vars = ['lexical_richness', 'WPM', 'positive', 'neutral', 'negative']

plot_dim = 331
for var in lyric_vars:
    plt.subplot(plot_dim)
    sns.distplot(bb[var]);
    sns.distplot(my[var]);
    plt.xlabel(var, fontsize=18, **hfont)
    plt.grid(True)
    plot_dim += 1

# stacked sentiment proportions 
sentiment = master[['isBillboard', 'positive', 'neutral', 'negative']]
sentiment.groupby('isBillboard').mean().plot.bar()
#sentiment.plot.bar(x = 'isBillboard', label=sentiment['isBillboard'], stacked=True)
#sentiment.plot.bar(x = 'isBillboard', stacked=True)
plt.show()


for i in range(len(my.lyrics)):
    if isinstance(my.lyrics[i], float):
        print(i, my.song[i], my.lyrics[i])
    else:
        None

# Common words from common artists
a = bb.groupby('artist').size()
n = a.apply(lambda x: 1).sum()
bb_artists = bb.groupby('artist').size()
my_artists = my.groupby('artist').size()

bb_topArtists = pd.DataFrame()
bb_topArtists['artist'] = ['drake', 'maroon 5', 'ariana grande', 'taylor swift', 'imagine dragons']
bb_topLyrics = list()
for artist in bb_topArtists['artist']:
    lyrics = '\n'.join(bb[bb['artist'] == artist]['lyrics'])
    bb_topLyrics.append(lyrics)
bb_topArtists['lyrics'] = bb_topLyrics

my_topArtists = pd.DataFrame()
my_topArtists['artist'] = ['wild child', 'dyan', 'sjowgren', 'many voices speak', 'phantogram']
my_topLyrics = list()
for artist in my_topArtists['artist']:
    lyrics = '\n'.join(my[my['artist'] == artist]['lyrics'])
    my_topLyrics.append(lyrics)
my_topArtists['lyrics'] = my_topLyrics

# Most common words: wordcloud
colors1 = ['purple', 'firebrick']
colors2 = ['green', 'blue']
bb_artistLabs = ['Drake', 'Maroon 5', 'Ariana Grande', 'Taylor Swift', 'Imagine Dragons']
my_artistLabs = ['Wild Child', 'DYAN', 'Sjowgren', 'Many Voices Speak', 'Phantogram']
for i in range(len(my_topArtists)):
    bb_wc = WordCloud(width=1000, height=500, collocations = False).generate(bb_topArtists.lyrics[i])
    my_wc = WordCloud(width=1000, height=500, collocations = False).generate(my_topArtists.lyrics[i])
    bb_wc.to_file('Images/WordClouds/' + bb_topArtists.artist[i] + ".png")
    my_wc.to_file('Images/WordClouds/' + my_topArtists.artist[i] + ".png")
    
    plt.figure(figsize=(2,6))
    bb_group = bb[['artist', 'positive', 'negative']].groupby('artist').mean().reset_index()
    bb_sent = bb_group[bb_group.artist== bb_topArtists.artist[i]]
    bb_sent.mean().plot.bar(color=colors1,alpha=0.6, title = bb_artistLabs[i])
    plt.ylabel('% of Words')
    plt.savefig('Images/Distributions/sentiment_' + bb_topArtists.artist[i] + '.png')
    plt.clf()
    
    plt.figure(figsize=(2,6))
    my_group = my[['artist', 'positive', 'negative']].groupby('artist').mean().reset_index()
    my_sent = my_group[my_group.artist == my_topArtists.artist[i]]
    my_sent.mean().plot.bar(color=colors2,alpha=0.6, title = my_artistLabs[i])
    plt.ylabel('% of Words')
    plt.savefig('Images/Distributions/sentiment_' + my_topArtists.artist[i] + '.png')
    plt.clf()