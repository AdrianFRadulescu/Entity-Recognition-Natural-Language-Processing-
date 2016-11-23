import nltk
from src.WSJEntity import WSJEntity


import re
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
from nltk.tokenize import _treebank_word_tokenize as tree_tok
from nltk.corpus.reader import PlaintextCorpusReader
from nltk.corpus.reader import WordListCorpusReader
from nltk.corpus.reader.wordnet import *


def complete_id(nr):
    rez = 'wsj_'
    if nr < 10:
        rez = rez + '000' + str(nr)
    elif nr < 100:
        rez = rez + '00' + str(nr)
    elif nr < 1000:
        rez = rez + '0' + str(nr)
    else:
        rez = rez + str(nr)

    return rez + '.txt'


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
    data = []
    for i in range(1, file_count+1):
        data = data + pattern.findall(nltk.data.load(paths[0]+complete_id(i), format='text'))

    # from every tag form the list find the two sub-strings
    # that correspond to the snd_pattern
    raw_entities = [list(map(lambda s: (s[:len(s)-1])[1:], l)) for l in (re.findall(snd_pattern, tag) for tag in data)]

    # extract data from names folders
    del data
    data = PlaintextCorpusReader(paths[1], '.*')

    raw_entities += [
        ['PERSON', w]
        for w in (
            data.words('names.male') +
            data.words('names.female') +
            data.words('names.family')
        )
    ]
    '''+ [
        ['PERSON', fn + sn]
        for fn in data.words('names.male') + data.words('names.female')
        for sn in data.words('names.family')]
    '''
    # create a data structure that contains the entities
    # and grants quick access to them

    return raw_entities


def untagged_reading(path=''):

    """
    Read the untaged data

    :param path: the root of the directory where the files are located
    :return : a corpus containing all the words in the loaded files

    """

    word_list = PlaintextCorpusReader(path, '.*\.txt')
    return word_list

