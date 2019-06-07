import numpy as np
import pandas as pd
import bs4
import requests
import re

url_base = 'https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_{}'

htmls = dict()
for year in range(2013, 2019):
    url = url_base.format(year)
    html = requests.get(url=url).content
    htmls[year] = bs4.BeautifulSoup(html, "lxml")

dfs = list()    # for collecting dataframes

# Parse wiki tables
for year, soup in htmls.items():
    # collect all relevant table rows into a list
    data = htmls[year]\
        .find('table', {'class':'wikitable sortable'})\
        .find_all('tr')
    rows = [datum.contents for datum in data]
    
    # the first, and every other <tr> object contains no data
    rows = [row[1::2] for row in rows][1:]
    
    # parse each row and store data in lists
    ranks = list()
    songs = list()
    artists_base = list() # collects only primary artist
    artists_all = list() # collects primary and featured artists
    for row in rows:
        # ranks must be cast as strings because of "Tie" as a possible value
        ranks.append(str(row[0].contents[0]))
        artists_all.append(' '.join(row[2].findAll(text=True)))
        
        # most primary artist data is a hyperlink, but some are just plaintext
        if not isinstance(row[2].contents[0], bs4.NavigableString):
            artists_base.append(row[2].contents[0].get('title'))
        else:
            artists_base.append(str(row[2].contents[0]))
        if len(row[1].contents) == 1:
            songs.append(str(row[1].contents[0]))
        else:
            songs.append(str(row[1].contents[1].findAll(text=True)[0]))
    
    # remove extra quotation marks from beginning and end of song titles
    songs = [song.strip("\"") for song in songs]
    
    # convert collected data for each year into its own dataframe
    # to be combined later
    data = dict(rank=ranks,
                song=songs,
                artist_base=artists_base,
                artist_all=artists_all,
                year=year)
    df = pd.DataFrame(data)
    dfs.append(df)

print("indent")

# Combine parsed data
billboard = pd.concat(dfs, axis=0)
billboard[['song', 'artist_all', 'artist_base']]\
    = billboard[['song', 'artist_all', 'artist_base']].applymap(str.lower)

# Remove disambiguations
billboard[['artist_base', 'artist_all']]\
    = billboard[['artist_base', 'artist_all']].applymap(
        lambda x: re.sub(r'\(.*', '', x).strip()
    )
        
# Fixing case-by-case issues
billboard.loc[billboard.artist_base == 'donald glover', 'artist_base'] = 'childish gambino'
billboard = billboard.reset_index()

# write to csv
billboard.to_csv('Data/billboard.csv', index=None)