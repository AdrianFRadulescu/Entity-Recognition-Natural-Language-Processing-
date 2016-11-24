import sys
import http.client, urllib.request, urllib.parse, urllib.error, json
import ssl

from pprint import pprint
from src.tagging import concat


# use a prefix list in order to search the wikipedia in all the common european languages with latin alphabet
prefixes = ['en', 'nl', 'pl', 'fr', 'de', 'pt', 'ro', 'no', 'sv', 'it', 'vi', 'es', 'hu', 'fi', 'da', 'sk',
                 'lt', 'hr']

# common attributes for filtering the titles

ORGANIZATION_attributes = ['Organization', 'Organizational behavior', 'Intergovernmental organization', 'Standards organization',
 'Organization development', 'International organization', 'Nonprofit organization', 'National Organization for Women',
 'Knowledge organization', 'Community organization', 'organization ethics', 'ethics', 'behavior', 'Nonprofit', 'standards']

LOCATION_attributes = ['altitude', 'settlement', 'history']

PERSON_attributes = ['house', 'spouse', 'wife', 'Mrs.', 'Mrs', 'Mr', 'Mr.', 'home', 'husband', 'position', 'function', 'employed', 'job',
                     'ocupation']


def contains_at_least_one_attribute(title=None):

    return []


def get_url(domain, url):

    # Headers are used if you need authentication
    headers = {}

    # If you know something might fail - ALWAYS place it in a try ... except
    try:
        conn = http.client.HTTPSConnection(domain, context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH))
        conn.request("GET", url, "", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        # These are standard elements in every error.
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

        # Failed to get data!
        return None


def find_inf(entity=None):

    query = concat(list(map(lambda x: str(x[0])+"%20", entity)))

    # This makes sure that any funny characters (including spaces) in the query are
    # modified to a format that url's accept.
    query = urllib.parse.quote_plus(query)

    url_data = []

    for pref in prefixes:

        # Call our function.
        data = get_url(pref + '.wikipedia.org', '/w/api.php?action=query&list=search&format=json&srsearch=' + query)

        # We know how our function fails - graceful exit if we have failed.

        if url_data is not None:
            url_data += [data]

    # http.client socket returns bytes - we convert this to utf-8
    url_data = list(map(lambda x: x.decode("utf-8"), url_data))

    # Convert the structured json string into a python variable
    url_data = [json.loads(ud) for ud in url_data]

    # Now we extract just the titles
    #titles = [i['title'] for i in url_data['query']['search']]
    titles = [[i['title'] for i in ud['query']['search']] for ud in url_data]

    #x = [[i for i in ud['query']['search']] for ud in url_data]

    #titles = list(filter(lambda x: x != [] and urllib.parse.quote_plus(x[0])+'+' == query, titles))


    # Make sure we can plug these into urls:
    #url_titles = [urllib.parse.quote_plus(i) for i in titles]
    #pprint(url_titles)
    return titles
