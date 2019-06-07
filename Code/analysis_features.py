import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# loading data
bb = pd.read_csv('Data/bbMaster.csv')
my = pd.read_csv('Data/myMaster.csv')

plt.figure(1, figsize=(20, 10),)

hfont = {'fontname':'DejaVu Sans'}

## plots
audio_vars1 = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'key',
               'liveness', 'loudness', 'mode', 'popularity']
audio_vars2 = ['speechiness', 'tempo', 'time_signature', 'valence', 'duration_sec',
               'release_year']
audio_vars = audio_vars1+audio_vars2
lyric_vars = [ 'lexical_richness', 'WPM', 'positive', 'negative', 'neutral', 'sentiment']

audio_labs = ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Key',
               'Liveness', 'Loudness', 'Mode', 'Popularity','Speechiness', 'Tempo', 
               'Time Signature', 'Valence', 'Duration Sec','Release Year']
lyric_labs = [ 'Lexical Richness', 'WPM', 'Positive', 'Negative', 'Neutral', 'Sentiment']

plt.figure(1, figsize=(40, 30),)
plot_dim = 1
for i in range(len(audio_vars)):
    plt.subplot(5,3,plot_dim)
    sns.distplot(bb[audio_vars[i]]);
    sns.distplot(my[audio_vars[i]]);
    plt.xlabel(audio_labs[i], fontsize=24, **hfont)
    plt.grid(True)
    plot_dim += 1
plt.savefig('Images/Distributions/audio_var.png')

plt.figure(1, figsize=(40, 20),)
plot_dim = 1
for i in range(len(lyric_vars)):
    plt.subplot(3,3,plot_dim)
    sns.distplot(bb[lyric_vars[i]]);
    sns.distplot(my[lyric_vars[i]]);
    plt.xlabel(lyric_labs[i], fontsize=18, **hfont)
    plt.grid(True)
    plot_dim += 1
plt.savefig('Images/Distributions/lyric_var.png')

# correlation maps
bb_corr = bb[audio_vars1 + ['speechiness', 'tempo', 'time_signature', 'valence', 
                            'duration_sec', 'lexical_richness', 'WPM', 'sentiment']].corr()
my_corr = my[audio_vars1 + ['speechiness', 'tempo', 'time_signature', 'valence', 
                            'duration_sec', 'lexical_richness', 'WPM', 'sentiment']].corr()

plt.figure(1, figsize=(20, 10),)
ax = plt.axes()
sns.heatmap(bb_corr, ax = ax)
ax.set_title('Billboard 100',fontsize=30)
plt.savefig('Images/Distributions/bb_corr_map.png')

plt.figure(1, figsize=(20, 10),)
ax = plt.axes()
sns.heatmap(my_corr, vmax = 1, vmin = -0.45, ax = ax)
ax.set_title('My Playlist',fontsize=30)
plt.savefig('Images/Distributions/my_corr_map.png')

# Welch t-tests for different means audio features:
ttest_df = pd.DataFrame()
ttests = list()
for var in audio_vars1+audio_vars2+lyric_vars:
    t = stats.ttest_ind(bb[var],my[var], equal_var=False)[1]
    ttests.append(t)
ttest_df['feature'] = audio_vars1+audio_vars2+lyric_vars
ttest_df['p-val'] = ttests
ttest_df




