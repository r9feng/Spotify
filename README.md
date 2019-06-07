# Comparison of Personal Music Profile with Billboard 100 Songs

An exploratory deep dive into audio and lyrical features of my personal favorite songs and of popular Billboard Top 100 songs.

I would describe my music taste as quite open, I tend to enjoy various types of music. In general, I have a propensity for lesser-known, independent (or indie) music. In terms of genres, I predominantly listen to indie rock or folk, but often find myself appreciating any piece of music with narrative lyrics, rich orchestrations or dynamic melody progressions. My curated Favorites playlist I contains 100 songs covering a wide spectrum of music genres including pop, rock, hip-hop, jazz rap, and folk. 

Table of Contents
-----------------

  * [Data Collection](#data-collection)
    * [Billboard Data](#billboard-data)
    * [Lyric Data](#lyric-data)
    * [Spotify Data](#spotify-data)
  * [Feature Engineering](#feature-engineering)
  * [Feature Analysis](#feature-analysis)
    * [Univariate Data](#univariate-data)
        * [Audio Features](#audio-features)
        * [Lyrical Features](#lyrical-features)
     * [Multivariate Data](#multivariate-data)
* [Lyrics: Closer Look](#lyrics-closer-look)
* [Clustering](#clustering)
    * [Feature Selection](#feature-selection)
    * [K-Means](#k-means-clustering)
* [Visualizing High Dimensions](#Visualizing-high-dimensions)
* [Conclusions](#conclusions)



## Data Collection

The data is collected from three sources: Billboard songs/artists are scraped from Wikipedia, lyrics are retrieved from the Genius API, and audio features and songs/artists from my own playlists are retrieved from Spotify's Web API.

Once the data was collected, it was cleaned to ensure that there were no missing/problematic fields. Some additional derived features were calculated (more details below). 

### Billboard Data

The popular music data used consisted of Billboard Year-End Hot 100 Singles from 2013 to 2018 and each single's corresponding lyrics. The range of years aligns with my undergraduate timeline and where I think began developing my musical profile. I scraped the data from relevant [Wikipedia tables](https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2018). I created a Python script and used the BeautifulSoup library to parse the Wikipedia html page. 

<p align="center">
  <img src="Data/Wiki_screen.png?raw=true" width="600" /> 
</p>

### Lyric Data

After retrieving songs, lyrical data is retrieved from Genius.com using the Genius API and searching by 

### Spotify Data

I curated a personal favorites playlist in Spotify and retrieved song titles and artists using the Spotify API and the Spotipy library. After retreiving Billboard 100 data and my own playlist, audio features for all songs were fetched from Spotify's music catalog with the Get Audio Features for a Track endpoint to retrieve song information in a JSON format. 

For the purposes of this study, the following audio features were retrieved: 

| Feature  | Definition by Spotify  |
|:-:|---|
| Energy |Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy. |
| Danceability | Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.  |
| Valence  |  A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).  |
| Tempo  | The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration. |
| Popularity  | The popularity of a track is a value between 0 and 100, with 100 being the most popular. The popularity is calculated by algorithm and is based, in the most part, on the total number of plays the track has had and how recent those plays are.  |
| Instrumentalness  | 	Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.  |
|  Acousticness | 	A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.  |
| Liveness  | Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live. |
| Speechiness | Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. |
| Key| The estimated overall key of the track. Integers map to pitches using standard Pitch Class notation . E.g. 0 = C, 1 = C♯/D♭, 2 = D|
| Mode| Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived.|

## Feature Engineering

Below are derived features, predominantly from raw lyrics. For instance, dividing the number of words used with the vocabulary gives us a measure of the lexical richness of each artist (i.e., what proportion of the words used in the songs are distinct). 

For sentiment analysis, I used NLTK's sentiment analyzer gives a normalized unidimensional metric of sentiment of a given sentence. In this case, I calculated percentage of words associated with (positive, negative, neutral)
 emotions.

| Feature  | Meaning  |
|:--:|---|
| Duration | Song duration from Spotify in seconds |
| Lexical Richness | Ratio of unique non-stopwords to total words |
| WPM | Number of words per minute |
| Positivity  | Percentage of words associated with positive sentiments |
| Negativity  | Percentage of words mssociated with negative sentiments |
| Neutrality  | Percentage of words associated with neutral sentiments |
| Sentiment   | Positivity - Negativity |

Final dataset includes 695 songs (495 Billboard, 100 My Playlist) with each row representing a single song. It contains the following variables: 

|  |  |  |  |  |
|-|---| -- |-|---|
|  Song |  Energy | Popularity | Lyrics| Lexical Richness  |
|  Artist | Liveness |  Key | Sentiment  |  WPM |
|  Tempo | Instrumentalness  |  Mode |  Positivity |  Release year |
|  Danceability | Acousticness  | Time Signature  | Neutrality  | Duration  |
|  Valence | Loudness  | Speechiness  |  Negativity |   |


# Feature Analysis

## Univariate Data

Began by examining the distributions of each audio and lyrical feature, comparing Billboard 100 set with my playlist.

### Audio Features

Blue = Billboard 100

Orange = My Playlist

<p align="center">
  <img src="Images/Distributions/audio_var.png?raw=true" width="1000" />
</p>

It is interesting to see similar distributions of most audio features (tempo too!). My music appears to be slightly less danceable, lower energy, and quieter. The only significantly different feature is popularity: my music is expectedly much less popular.

### Lyrical Features

Explain sentiment analysis methodology

<p align="center">
  <img src="Images/Distributions/lyric_var.png?raw=true" width="1000" /> 
</p>

Here we some differences in lexical richness and words per minute. My music tends to be more lyrically complex but slower "spoken". As for sentiment, my music is more neutral, with less positive and negative lyrical expressions.

Performing Welch t-tests for differences in means of these features yields the following significant differences (p-value < 0.05):

|Feature|
|--|
| Popularity | 
| WPM | 
| Loudness |
| Energy |
| Danceability | 
| Lexical Richness|
| Acousticness |
| Instrumentalness |

Which agree with the visual distribution comparison! 

## Multivariate Data

Correlation maps:

<p align="center">
  <img src="Images/Distributions/bb_corr_map.png?raw=true" width="1200" />
  <img src="Images/Distributions/my_corr_map.png?raw=true" width="1200" /> 
</p>

The correlation structure of both datasets appears to be similar. An interesting difference being that song duration and danceability are much more negatively correlated amongst my songs compared to Billboard songs which suggests I tend to enjoy high danceability for shorter songs.

Interesting trends in both sets:
- valence, sentiment uncorrelated: musical emotion not tied to lyrical emotion?

# Lyrics: Closer Look

Below are the word clouds of the entirety of the Billboard 100 songs and my playlist songs.

Billboard WordCloud
<p align="center">
  <img src="Images/WordClouds/all_bbWC.png?raw=true" width="600" />
</p>
My Favorites WordCloud
<p align="center">
  <img src="Images/WordClouds/all_myWC.png?raw=true" width="600" /> 
</p>

Many of the most common words in lyrics are the same for both sets of songs ("know", "Love", "Want/Wanna", "Oh"). 

### Favorite artists
I also examined lyrical features of the top 5 most reoccuring artists on the Billboard 100 and my own playlists.

<table>
<tr><th>Billboard 100 </th><th>My Playlist</th></tr>
<tr><td>

|Artist| # Songs |
|--|--|
| Drake | 19 |
| Maroon 5 | 13 |
| Ariana Grande | 11 |
| Taylor Swift | 11 |
| Imagine Dragons | 11 |


</td><td>

|Artist| # Songs |
|--|--|
| Wild Child | 6 |
| DYAN | 4 |
| Sjowgren | 4 |
| Many Voices Speak | 3 |
| Phantogram | 3 |

</td></tr> </table>

<p align="center">
  <img src="Images/WordClouds/drake.png?raw=true" width="355"/> 
  <img src="Images/Distributions/sentiment_drake.png?raw=true" width="72" /> 
  <img src="Images/Distributions/sentiment_wild child.png?raw=true" width="72" /> 
  <img src="Images/WordClouds/wild child.png?raw=true" width="355" />
</p>

<p align="center">
  <img src="Images/WordClouds/maroon 5.png?raw=true" width="355" />
   <img src="Images/Distributions/sentiment_maroon 5.png?raw=true" width="72" /> 
    <img src="Images/Distributions/sentiment_dyan.png?raw=true" width="72" /> 
  <img src="Images/WordClouds/dyan.png?raw=true" width="355" />
</p>

<p align="center">
  <img src="Images/WordClouds/ariana grande.png?raw=true" width="355" />
  <img src="Images/Distributions/sentiment_ariana grande.png?raw=true" width="72" /> 
    <img src="Images/Distributions/sentiment_sjowgren.png?raw=true" width="72" /> 
  <img src="Images/WordClouds/sjowgren.png?raw=true" width="355" />
</p>


<p align="center">
  <img src="Images/WordClouds/taylor swift.png?raw=true" width="355" />
  <img src="Images/Distributions/sentiment_taylor swift.png?raw=true" width="72" /> 
    <img src="Images/Distributions/sentiment_many voices speak.png?raw=true" width="72" /> 
  <img src="Images/WordClouds/many voices speak.png?raw=true" width="355" />
</p>


<p align="center">
  <img src="Images/WordClouds/imagine dragons.png?raw=true" width="355" />
  <img src="Images/Distributions/sentiment_imagine dragons.png?raw=true" width="72" /> 
    <img src="Images/Distributions/sentiment_phantogram.png?raw=true" width="72" /> 
  <img src="Images/WordClouds/phantogram.png?raw=true" width="355" />
</p>

It was surprising to see Drake lyrics are more positive while Taylor Swift lyrics are more negative. Furthermore, it's evident that different artists have highly varying lyrical content and sentiment. Perhaps, differences in musical profile disappear once a wide variety of artists and genres are incorporated? We'll look at some unsupervised clustering to identify natural groups of songs to investigate this further.

# Clustering 

## Feature Selection

We have 16 variables available to cluster upon, which drastically increases complexity and reduces interpretability of clusters. Thus we'll need to subset the features. 

I chose to use the Recursive Feature Elimination (RFE) method which recursively removing attributes and building a model on those attributes that remain. It uses the model accuracy to identify which attributes (and combination of attributes) contribute the most to predicting the target attribute. In this case, I used sklearn's LogisticRegression and RFE library to build a logistic regression model which attempts to predict whether a song is from the Billboard 100 or from my playlist. The following features were found to have the most impact on the mental health class variable (popularity omitted).

| Rank  | Song Attribute  |
|-|---|
|  1 | Words Per Minute  |
|  2 | Loudness |
|  3 | lexical_richness  |
|  4 | danceability  |
|  5 | Valence  |
|  6 | energy  |
|  7 | sentiment  |
|  8 | Tempo  |
|  9 | Instrumentalness  |
|  10 | Liveness  |
|  11 | Duration  |
|  12 | key  |
|  13 | speechiness  |
|  14 | time_signature |
|  15 | acousticness  |
|  16 | mode (remove) |

As expected, the probabilistic classification variables like instrumentalness, liviness, acousticness were least important. The top eight features were kept while rest were removed to reduce complexity of our clusters.

Aside: I attempted to predict the binary classifiction with 5 fold cross validation using the logistic regression. This yielded very poor predictions with an AUC of 0.32 (fpr, tpr better?) which further reinforces the lack of difference between the two sets as a whole.

## K-Means Clustering

I chose to cluster with the k-means algorithm to exhibit natural groupings of songs based on features. Note that song popularity is omitted since the primary goal is to examine differences in terms of audio and lyrical features. Popularity would be a trivial feature on which to categorize. In order to find the optimal number of clusters the Elbow Method was used. The Elbow method looks at the percentage of variance explained as a function of the number of clusters. The optimal number should form an "elbow", which indicates the point at which additional variance explained by including an additional cluster has less of an impact on the cluster center. The graph to find the "elbow" is shown below:

<p align="center">
  <img src="Images/Clusters/clusterElbow.png?raw=true" width="400" />
</p>

For both datasets, the "elbow" is most visible at k=3. Thus I ran the algorithm with 3 clusters and examined bivariate plots to visualize any clear partition of clusters on two variables. For most pairs of variables, the clusters were highly overlapping as shown below:

<p align="center">
  <img src="Images/Clusters/bb_overlap_DV.png?raw=true" width="400" />
  <img src="Images/Clusters/my_overlap_EV.png?raw=true" width="400" /> 
</p>

However, WPM vs. Tempo exhibited clearer homogeneous clusters for both sets of data as shown below:  

<p align="center">
  <img src="Images/Clusters/bb_sep_TW.png?raw=true" width="400" />
  <img src="Images/Clusters/my_sep_TW.png?raw=true" width="400" /> 
</p>


It's interesting to see that tempo and words per minute are the main factors that divides both dataset into three clusters, implying that there exist three types of songs: 

- Low WPM, Low Tempo: (eg. )
- Low WPM, High Tempo: (eg. )
- High WPM, Any Tempo: Hip-hop or Rap songs. High lyrical content at all tempos (eg. Logic, Travis Scott, BROCKHAMPTON)


# Visualizing High Dimensions

In order visualize high dimensional the grouping structure of the songs, I chose to use t-SNE to project songs from both Billboard 100 and my playlist. This yields a  2D map of all songs while preserving representations of relative differences between data.

 It converts similarities between data points to joint probabilities and tries to minimize the Kullback-Leibler divergence between the joint probabilities of the low-dimensional embedding and the high-dimensional data.

Care needs to be taken when interpreting these plots but essentially each point represents a song and relative distances between two songs indicate how similar those two songs are (lyrically and audibly)

<p align="center">
  <img src="Images/DimReduction/all_tsne.png?raw=true" width="1000" />
</p>

Projecting songs from both billboard 100 and my playlist shows some groupings of my songs. ie. the few rap and hip-hop songs are very closely grouped. Below is the t-SNE of the Billboard 100 clusters:

<p align="center">
  <img src="Images/DimReduction/bbclusters_tsne.png?raw=true" width="1000" />
</p>

<p align="center">
  <img src="Images/DimReduction/myclusters_tsne.png?raw=true" width="1000" />
</p>

Finally, I projected all of the top 5 artists from Billboard 100 and My playlists (10 artists total).

<p align="center">
  <img src="Images/DimReduction/artists_tsne.png?raw=true" width="1000" />
</p>

# Conclusions

In general, I found that while audio and lyrical differences are present between segmented music groups (ie. Artists), differences in musical profile seem to disappear once a wide variety of artists and genres are incorporated. My personal playlist 

In examining During analysis, I noticed 



