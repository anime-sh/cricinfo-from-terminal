import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

home_url = "http://static.cricinfo.com/rss/livescores.xml"
home_page = requests.get(home_url)
soup = BeautifulSoup(home_page.content, 'xml')
links = soup.find_all('link')
titles = soup.find_all('title')

for i in range(1, len(links)):
    print(f"ID {i} , MATCH: {titles[i].contents[0]}")

id = int(input("Enter Match ID "))

r = requests.get(links[id].contents[0])
url = r.url.split('/')
game_ids = {}
for x in url:
    if(x.isdigit()):
        if(not ('series' in game_ids)):
            game_ids['series'] = x
        elif(not('match' in game_ids)):
            game_ids['match'] = x

try:
    match_url = 'https://www.espncricinfo.com/series/' + \
        str(game_ids['series']) + '/scorecard/' + str(game_ids['match'])
    page = requests.get(match_url)
    df_list = pd.read_html(page.text, match='BATSMEN')
    for df in df_list:
        df.drop(df.filter(regex="Unnamed"), axis=1, inplace=True)
        df = df.dropna()
        df = df.reset_index(drop=True)
        df = df[:-1]
        if(str(df.at[len(df.index)-1, 'BATSMEN']).startswith('Yet to bat') or str(df.at[len(df.index)-1, 'BATSMEN']).startswith('Did not bat')):
            df = df[:-1]
        print(df)

    print("Bowling Data")
    df_list2 = pd.read_html(page.text, match='BOWLING')
    for df in df_list2:
        print(df)
except:
    print("Couldnt access scorecard / Match hasnt started yet")
