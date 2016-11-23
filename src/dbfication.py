import sys
import http.client, urllib.request, urllib.parse, urllib.error, xml
import ssl

from pprint import pprint
from src.tagging import concat


def get_url(domain,url):

    try:
        connection = http.client.HTTPSConnection(domain, context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH))
        connection.request("GET", url, "")
        response = connection.getresponse()
        data = response.read()
        connection.close()
        return data

    except Exception as e:

        #Falied to get data

        print("[Err no {0}]".format(e.errno, e.strerror))
        return None

def find_inf(entity=None):

    query = "Code Geass"

    #modify the query to a format that is ulr accepted
    query = urllib.parse.quote_plus(query)

    url_data = get_url('dbpedia.org', '/api/search.asmx/PrefixSearch?QueryClass=&MaxHits=5&QueryString=' +query)

    if url_data is None:
        print('esec')

    print( url_data.decode('utf-8'))

find_inf()