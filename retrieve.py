from query import parser
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd



def print_name_and_pic(player_id):
    json_url = "http://core.espnuk.org/v2/sports/cricket/athletes/"+player_id
    json_player = requests.get(json_url).json()
    print(f"Name: {json_player['name']}")
    print(f"Photo: {json_player['headshot']['href']}")


def get_relevant_stats(query_url):
    page = requests.get(query_url)
    df_list = pd.read_html(page.text,match='Career averages')
    if(len(df_list)<=0):
        print("couldnt retrieve anything")
    df=df_list[0]
    df.drop(df.filter(regex="Unnamed"),axis=1, inplace=True)
    if(len(df.index)>1):
        print(df.loc[1])
    else:
        print(df.loc[0])

querying_url, player_id = parser(sys.argv[1])
print(querying_url)
print_name_and_pic(player_id)
get_relevant_stats(querying_url)