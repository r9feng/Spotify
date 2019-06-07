import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE

# reading data
bb = pd.read_csv('Data/bbMaster.csv')
my = pd.read_csv('Data/myMaster.csv')
master = pd.read_csv('Data/master.csv')
clusterLabel = pd.read_csv('Data/clusterLabel.csv')

# setup data
x = master.drop(columns=['artist', 'song', 'release_year', 'lyrics'], index=None)
X_embedded = TSNE(n_components=2,random_state=1234).fit_transform(x)

fig = plt.figure(figsize=(35, 25))
ax = plt.axes(frameon=False)
plt.setp(ax, xticks=(), yticks=())
plt.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=0.9,
                wspace=0.0, hspace=0.0)
plt.scatter(X_embedded[:, 0], X_embedded[:, 1], s=80,   marker="8")

## dynamic
for i in range(len(master)):
    if master.isBillboard[i] == 0:
        target_word = master.song[i]
        xx = X_embedded[i, 0]
        yy = X_embedded[i, 1]
        plt.annotate(target_word, (xx,yy), size=10, xytext=(-90,90), 
            textcoords='offset points', ha='center', va='bottom',
            bbox=dict(boxstyle='round4', fc='white', alpha=0.3),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', 
                            color='red'))
fig.savefig('Images/DimReduction/all_tsne.png')

plt.clf()
## No clusters

for i in range(len(master)):
    if master.isBillboard[i] == 0:
        target_word = master.song[i]
        xx = X_embedded[i, 0]
        yy = X_embedded[i, 1]
        plt.annotate(target_word, (xx,yy), size=10, xytext=(-90,90), 
            textcoords='offset points', ha='center', va='bottom',
            bbox=dict(boxstyle='round4', fc='white', alpha=0.3),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', 
                            color='red'))

fig.savefig('Images/DimReduction/all_tsne.png')


## billboard clusters:

for i in range(len(master)):
    if master.isBillboard[i] == 1:
        if clusterLabel.cluster[i] == 0:
            target_word = master.song[i]
            xx = X_embedded[i, 0]
            yy = X_embedded[i, 1]
            plt.annotate(target_word, (xx,yy), size=10, xytext=(-90,90), 
                textcoords='offset points', ha='center', va='bottom',
                bbox=dict(boxstyle='round4', fc='blue', alpha=0.3),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', 
                                color='blue'))
        if clusterLabel.cluster[i] == 1:
            target_word = master.song[i]
            xx = X_embedded[i, 0]
            yy = X_embedded[i, 1]
            plt.annotate(target_word, (xx,yy), size=10, xytext=(-90,90), 
                textcoords='offset points', ha='center', va='bottom',
                bbox=dict(boxstyle='round4', fc='red', alpha=0.3),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', 
                                color='red'))
        if clusterLabel.cluster[i] == 2:
            target_word = master.song[i]
            xx = X_embedded[i, 0]
            yy = X_embedded[i, 1]
            plt.annotate(target_word, (xx,yy), size=10, xytext=(-90,90), 
                textcoords='offset points', ha='center', va='bottom',
                bbox=dict(boxstyle='round4', fc='green', alpha=0.3),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', 
                                color='green'))

fig.savefig('Images/DimReduction/bbclusters_tsne.png')

## my clusters

for i in range(len(master)):
    if master.isBillboard[i] == 0:
        if clusterLabel.cluster[i] == 0:
            target_word = master.song[i]
            xx = X_embedded[i, 0]
            yy = X_embedded[i, 1]
            plt.annotate(target_word, (xx,yy), size=10, xytext=(-90,90), 
                textcoords='offset points', ha='center', va='bottom',
                bbox=dict(boxstyle='round4', fc='teal', alpha=0.3),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', 
                                color='teal'))
        if clusterLabel.cluster[i] == 1:
            target_word = master.song[i]
            xx = X_embedded[i, 0]
            yy = X_embedded[i, 1]
            plt.annotate(target_word, (xx,yy), size=10, xytext=(-90,90), 
                textcoords='offset points', ha='center', va='bottom',
                bbox=dict(boxstyle='round4', fc='purple', alpha=0.3),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', 
                                color='purple'))
        if clusterLabel.cluster[i] == 2:
            target_word = master.song[i]
            xx = X_embedded[i, 0]
            yy = X_embedded[i, 1]
            plt.annotate(target_word, (xx,yy), size=10, xytext=(-90,90), 
                textcoords='offset points', ha='center', va='bottom',
                bbox=dict(boxstyle='round4', fc='orange', alpha=0.3),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', 
                                color='orange'))
##
fig.savefig('Images/DimReduction/myclusters_tsne.png')


## Exposition by artist:
top_artists = ['drake', 'maroon 5', 'ariana grande', 'taylor swift', 'imagine dragons',
               'wild child', 'dyan', 'sjowgren', 'many voices speak', 'phantogram']
artist_colors = ['red','blue','green','orange','purple',
                 'brown','silver','teal','yellow','magenta']
for art in range(len(top_artists)):
    for i in range(len(master)):
        if master.artist[i] == top_artists[art]:
            target_word = master.artist[i]
            xx = X_embedded[i, 0]
            yy = X_embedded[i, 1]
            plt.annotate(target_word, (xx,yy), size=10, xytext=(-90,90), 
                textcoords='offset points', ha='center', va='bottom',
                bbox=dict(boxstyle='round4', fc=artist_colors[art], alpha=0.3),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', 
                                color=artist_colors[art]))
fig.savefig('Images/DimReduction/artists_tsne.png')
