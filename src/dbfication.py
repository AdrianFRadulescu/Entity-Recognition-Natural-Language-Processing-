import sys
import http.client, urllib.request, urllib.parse, urllib.error, json
import ssl

from pprint import pprint
from src.tagging import concat


def get_url(domain, url):

    try:
        connection = http.client.HTTPSConnection(domain, context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH))
        connection.request("GET", url, "")
        #response = connection.getresponse()
        #data = response.read()
        connection.close()
        return True

    except Exception as e:

        #Falied to get data

        print("[Err no {0}]".format(e.errno, e.strerror,e.with_traceback()))
        return None


def find_inf(entity=None):

    query = "berlin"

    #modify the query to a format that is ulr accepted
    query = urllib.parse.quote_plus(query)

    url_data = get_url('lookup.dbpedia.org', '/api/search.asmx/KeywordSearch?QueryClass=place&QueryString=berlin')

    if url_data is None:
        print('adasd')

    #print(url_data.decode('utf-8'))

