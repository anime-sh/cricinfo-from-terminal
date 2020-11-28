import json
import urllib
import requests
import sys
import dateparser
from bs4 import BeautifulSoup
import datetime
with open('./data.json') as f:
    data = json.load(f)


def parser(query):
    basic = query.split("@")
    words = [x.strip() for x in basic]
    name = words[0]
    if(name.startswith('!')):
        woman = True
        name = name[1:]
    else:
        woman = False
    search_url = "http://stats.espncricinfo.com/stats/engine/stats/analysis.html?search=" + \
        name.replace(" ", "+") + ";template=analysis"
    search_page = requests.get(search_url)
    soup = BeautifulSoup(search_page.content, 'html.parser')
    links = soup.find_all(class_='statsLinks')
    player = None
    if(woman):
        for link in links:
            if(link.has_attr('href')):
                if("Women's Test matches player" == link.text):
                    player = link['href']
                    break
                elif("Women's One-Day Internationals player" == link.text):
                    player = link['href']
                    break
                elif("Women's Twenty20 Internationals player" == link.text):
                    player = link['href']
                    break
                else:
                    pass
    else:
        for link in links:
            if(link.has_attr('href')):
                if("Combined Test, ODI and T20I player" == link.text):
                    player = link['href']
                    break
                elif("Test matches player" == link.text):
                    player = link['href']
                    break
                elif("One-Day Internationals player" == link.text):
                    player = link['href']
                    break
                elif("Twenty20 Internationals player" == link.text):
                    player = link['href']
                    break
                else:
                    pass
    query_processed = {}
    # default values
    if(woman):
        query_processed["format"] = 9
    else:
        query_processed["format"] = 11
    for word in words[1:]:
        pro = word.split(" ")
        if(pro[0] in data['terms']):
            pass
        elif(pro[0].upper() in data['terms']):
            pro[0] = pro[0].upper()
        elif(pro[0].casefold() in data['terms']):
            pro[0] = pro[0].casefold()
        else:
            continue
        term = data['terms'][pro[0]]
        print(f"term is {term}, pro[0] is {pro[0]}")
        if(len(pro) == 1):  # single
            query_processed[term] = data[term][pro[0]]
        elif (term == 'cmd'):
            if(pro[0] == 'vs'):
                if(pro[1] in data['terms']):
                    pass
                elif(pro[1].upper() in data['terms']):
                    pro[1] = pro[1].upper()
                elif(pro[1].casefold() in data['terms']):
                    pro[1] = pro[1].casefold()
                query_processed["ctry"] = data["ctry"][pro[1]]
            elif(pro[0].startswith('y') or pro[0] == 'time'):
                discard, useful = word.split(None, 1)
                if(pro[0] == discard):
                    if('-' in useful):
                        y_start, y_stop = useful.split('-')
                        query_processed['start'] = dateparser.parse(
                            y_start).strftime("%d %B %Y")
                        query_processed['start'] = query_processed['start'].split(
                        )
                        query_processed['start'][1] = query_processed['start'][1][0:3]
                        query_processed['start'] = ' '.join(
                            query_processed['start'])
                        query_processed['stop'] = dateparser.parse(
                            y_stop).strftime("%d %B %Y")
                        query_processed['stop'] = query_processed['stop'].split()
                        query_processed['stop'][1] = query_processed['stop'][1][0:3]
                        query_processed['stop'] = ' '.join(
                            query_processed['stop'])
                    elif ('to' in useful):
                        y_start, y_stop = useful.split('to')
                        query_processed['start'] = dateparser.parse(
                            y_start).strftime("%d %B %Y")
                        query_processed['start'] = query_processed['start'].split(
                        )
                        query_processed['start'][1] = query_processed['start'][1][0:3]
                        query_processed['start'] = ' '.join(
                            query_processed['start'])
                        query_processed['stop'] = dateparser.parse(
                            y_stop).strftime("%d %B %Y")
                        query_processed['stop'] = query_processed['stop'].split()
                        query_processed['stop'][1] = query_processed['stop'][1][0:3]
                        query_processed['stop'] = ' '.join(
                            query_processed['stop'])
                    else:
                        query_processed['year'] = dateparser.parse(useful)
    url_dict = {}
    if(woman):
        if('format' in query_processed):    
            if(query_processed['format']==11):
                query_processed['format']=9
            elif(query_processed['format']==1):
                query_processed['format']=8
            elif(query_processed['format']==2):
                query_processed['format']=9
            elif(query_processed['format']==3):
                query_processed['format']=10
            else:
                pass   
    if('format' in query_processed):
        url_dict['class'] = query_processed['format']
    if('host' in query_processed):
        url_dict['host'] = query_processed['host']
    if('ctry' in query_processed):
        url_dict['opposition'] = query_processed['ctry']
    if('stadium' in query_processed):
        url_dict['home_or_away'] = query_processed['stadium']
    if('year' in query_processed):
        url_dict['year'] = query_processed['year']
    if('start' in query_processed):
        url_dict['spanmax1'] = query_processed['stop']
        url_dict['spanmin1'] = query_processed['start']
        url_dict['spanval1'] = 'span1'
    # print(str(query_processed))
    url = urllib.parse.urlencode(url_dict).replace(
        "&", ";").replace("%2B", "+")
    # print(str(url))
    # get playerid from name

    if(not player):
        print("Player not found please try again")
    else:
        starting, ending = player.split('?')
        components = starting.split('.', 1)
        components = components[0]
        components = components.split('/')
        player_id = None
        for component in components:
            if(component.isdigit()):
                player_id = component
                break
        starting += '?'
        total_url = "https://stats.espncricinfo.com" + \
            starting+url+';template=results;type=allround'
        return total_url, player_id
