__author__ = 'yk'

import requests
import json
import handicap


BASE = "http://130.211.166.43:8008/web/api.php/v1"


def get_route(params):
    url = BASE + "/connections"
    print ("Trying: " ,url)
    resp = requests.get(url, params=params)
    jsn = resp.json()
    if 'connections' not in jsn:
        return []
    cns = jsn['connections']
    handicap.annotate_connections(cns)
    return cns


def search_name(query):
    url = BASE + "/locations"
    resp = requests.get(url, params={'query': query})
    jsn = resp.json()
    if 'stations' not in jsn:
        return []
    return list(map(lambda x: x['name'], jsn['stations']))


if __name__ == '__main__':
    print(list(search_name("Zuri")))
    print(json.dumps(get_route({"from":"Lausanne","to":"Bern"})[0],indent=True))
