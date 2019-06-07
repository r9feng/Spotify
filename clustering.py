from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import itertools as it

bb_raw = pd.read_csv('Data/bbMaster.csv')
my_raw = pd.read_csv('Data/myMaster.csv')

keep = ['WPM',
        'loudness',
        'lexical_richness',
        'danceability',
        'valence',
        'energy',
        'sentiment',
        'tempo']

bb = bb_raw[keep]
my = my_raw[keep]

# K-means clustering: Billboard
elbow = pd.DataFrame()
num_clust = list()
ss_dist = list()
# "elbow" cluster optimization
for i in range(2,20):
    kmean = KMeans(n_clusters=i, init='k-means++', random_state=123)
    bb_kmean = kmean.fit(bb)
    num_clust.append(i)
    ss_dist.append(bb_kmean.inertia_)
    
plt.plot(num_clust,ss_dist) # elbow at 5?

KM3_bb = KMeans(n_clusters=3, init='k-means++', random_state=123)
bb_KM3 = KM3_bb.fit(bb)

# K-means clustering: My Music
elbow = pd.DataFrame()
num_clust = list()
ss_dist = list()
# "elbow" cluster optimization
for i in range(2,20):
    kmean = KMeans(n_clusters=i, init='k-means++', random_state=123)
    my_kmean = kmean.fit(my)
    num_clust.append(i)
    ss_dist.append(my_kmean.inertia_)
    
plt.plot(num_clust,ss_dist) # elbow at 3?
#plt.savefig('Images/Clusters/clusterElbow.png')

KM3_my = KMeans(n_clusters=3, init='k-means++', random_state=123)
my_KM3 = KM3_my.fit(my)

# bivariate plots of clusters
colors1 = ['blue','red', 'green']
colors2 = ['teal', 'purple', 'orange']
def kmeanBivariate(data, x, y, cluster_lab, colors, save):#, x_lab, y_lab):
    plt.scatter(data[x], data[y], c=cluster_lab, cmap=matplotlib.colors.ListedColormap(colors), s=75)
    plt.xlabel(x)
    plt.ylabel(y)
    #plt.show
    if save == True:
        return plt
    else:
        None

bivariates = it.combinations(list(bb.columns), 2)

for pairs in bivariates:
    kmeanBivariate(bb,pairs[0],pairs[1],KM3_bb.labels_,colors1,False)
    plt.show()
    
for pairs in bivariates:
    kmeanBivariate(my,pairs[0],pairs[1],KM3_my.labels_,colors2,False)
    plt.show()

# outputting clusterlabels
bb_clusterLabel = pd.DataFrame()
my_clusterLabel = pd.DataFrame()
bb_clusterLabel['cluster'] = KM3_bb.labels_
my_clusterLabel['cluster'] = KM3_my.labels_
bb_clusterLabel['song'] = bb_raw.song
my_clusterLabel['song'] = my_raw.song
clusterLabel = bb_clusterLabel.append(my_clusterLabel).reset_index()

#di = {}
#bb_clusterLabel.replace({"col1": di})
#my_clusterLabel.replace({"col1": di})

clusterLabel.to_csv('Data/clusterLabel.csv', index=None)

# numerical examination of clusters:
bb_KM3_centers = pd.DataFrame(bb_KM3.cluster_centers_)
my_KM3_centers = pd.DataFrame(my_KM3.cluster_centers_)

bb_KM3_centers.columns=bb.columns
my_KM3_centers.columns=my.columns

bb_KM3_centers.to_csv('Data/bb_km3centers.csv', index=None)
my_KM3_centers.to_csv('Data/my_km3centers.csv', index=None)

# output relevant plots:
plt.clf()
kmeanBivariate(bb,'danceability','valence',KM3_bb.labels_,colors1,True).savefig('Images/Clusters/bb_overlap_DV.png')
plt.clf()
kmeanBivariate(bb,'tempo','WPM',KM3_bb.labels_,colors1,True).savefig('Images/Clusters/bb_sep_TW.png')
plt.clf()

kmeanBivariate(my,'energy','valence',KM3_my.labels_,colors2,True).savefig('Images/Clusters/my_overlap_EV.png')
plt.clf()
kmeanBivariate(my,'tempo','WPM',KM3_my.labels_,colors2,True).savefig('Images/Clusters/my_sep_TW.png')
plt.clf()
    
