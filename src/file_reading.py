import nltk


import re
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
from nltk.tokenize import _treebank_word_tokenize as tree_tok
from nltk.corpus.reader import PlaintextCorpusReader
from nltk.corpus.reader import WordListCorpusReader
from nltk.corpus.reader.wordnet import *
from nltk.tokenize import word_tokenize
from nltk.corpus import names

from src.tagging import final_tagger


def training_data(paths=None, file_count=0):

    """
        Use the general pattern of a tag <ENAMEX\sTYPE=".*?">.*?</ENAMEX>
        in order to extract the bits of text containing the relevant information and
        group them into a list
        Chunk the elements of the list leaving only a tuple reprezented by the type of the entity
        and its name

        :param paths          the paths towards the file containing the training data
        :param file_count     the number of files to read
        :return               a list of lists where each element is a list formed from the type of the entity and its ful name
    """

    # extract training data from WSJ
    # pattern : the general pattern of a tag
    # snd_pattern : the approximate pattern of the desired information from the tag
    pattern = re.compile(r'<.*?TYPE=".*?">.*?</.*?>', re.ASCII)
    snd_pattern = re.compile(r'[>"].*?[<"]', re.ASCII)

    # the strings representing the tags extracted from the files

    text = PlaintextCorpusReader(paths[0], '.*\.txt')

    data = []
    for fid in text.fileids():
        data = data + pattern.findall(text.raw(fileids=fid),re.ASCII)

    # from every tag form the list find the two sub-strings
    # that correspond to the snd_pattern
    # use sets to eliminate redundancy
    raw_entities = list(set(list(map(lambda re: (re[0], re[1].lower()), list(map(lambda x: (x[0], x[1]), [list(map(lambda s: (s[:len(s)-1])[1:], l)) for l in (re.findall(snd_pattern, tag) for tag in data)]))))))

    # extract data from names folders
    del data
    data = PlaintextCorpusReader(paths[1], '.*')

    name_data = data.words('names.male') + data.words('names.female') + data.words('names.family')

    # extract the most common 350 organization tokens

    organization_words = list(map(lambda o: word_tokenize(o[1]), list(filter(lambda x: x[0] == 'ORGANIZATION', raw_entities))))

    organization_specific_tokens = []
    for wl in organization_words:
        organization_specific_tokens += wl

    organization_specific_tokens = list(map(lambda f: f[0], FreqDist(organization_specific_tokens).most_common(350)))

    location_words = list(map(lambda o: word_tokenize(o[1]), list(filter(lambda x: x[0] == 'LOCATION', raw_entities))))
    location_specific_tokens = []
    for wl in location_words:
        location_specific_tokens += wl

    location_specific_tokens = list(map(lambda f: f[0], FreqDist(location_specific_tokens).most_common(350)))

    # put the names in a dictionary for quicker access
    name_dict = {}
    for n in list(set(name_data + names.words())):
        if n.lower()[0] in name_dict:
            name_dict[n.lower()[0]] += [n.lower()]
        else:
            name_dict[n.lower()[0]] = [n.lower()]

    # put the location data in a dictionary for quicker access
    loc_dict = {}
    for l in location_specific_tokens[1:]:
        if l[0] in loc_dict:
            loc_dict[l[0]] += [l]
        else:
            loc_dict[l[0]] = [l]

    # put the organization data in a dictionary for quicker access
    org_dict = {}
    for o in organization_specific_tokens:
        if o[0] in org_dict:
            org_dict[o[0]] += [o]
        else:
            org_dict[o[0]] = [o]

    entity_dict1 = {
        'PERSON': list(map(lambda p: p[1], list(filter(lambda e: e[0] == 'PERSON', raw_entities)))),
        'LOCATION': list(map(lambda l: l[1], list(filter(lambda e: e[0] == 'LOCATION', raw_entities)))),
        'ORGANIZATION': list(
            map(lambda o: o[1], list(filter(lambda e: e[0] == 'ORGANIZATION', raw_entities))))
    }

    entity_dict2 = {}
    for l in ['PERSON', 'ORGANIZATION', 'LOCATION']:
        entity_dict2[l] = {}
        for e in entity_dict1[l]:
            if e[0] in entity_dict2[l]:
                entity_dict2[l][e[0]] += [e]
            else:
                entity_dict2[l][e[0]] = [e]

    return entity_dict2, org_dict, name_dict, loc_dict


def untagged_reading(path=''):

    """
    Read the untaged data

    :param path: the root of the directory where the files are located
    :return : a corpus containing all the words in the loaded files

    """

    word_list = PlaintextCorpusReader(path, '.*\.txt')
    return word_list

