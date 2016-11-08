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
    rez  = 'wsj_'
    if nr < 10:
        rez = rez + '000' + str(nr)
    elif nr < 100:
        rez = rez + '00' + str(nr)
    elif nr < 1000:
        rez = rez + '0' + str(nr)
    else:
        rez = rez + str(nr)

    return rez + '.txt'


def tag_reading_and_entity_extraction(path='', file_count=0):

    """
        Use the general pattern of a tag <ENAMEX\sTYPE=".*?">.*?</ENAMEX>
        in order to extract the bits of text containing the relevant information and
        group them into a list
        Chunk the elements of the list leaving only a tuple reprezented by the type of the entity
        and its name

        :param path           the path towards the file containing the training data
        :param file_count     the number of files to read
        :return               a list of lists where each element is a list formed from the type of the entity and its ful name

        :var pattern:       the general pattern of a tag
        :var snd_pattern:   the approximate pattern of the desired information from the tag
        :var data:          the strings representing the tags extracted from the files

    """
    pattern = re.compile(r'<.*?TYPE=".*?">.*?</.*?>', re.ASCII)
    snd_pattern = re.compile(r'[>"].*?[<"]', re.ASCII)

    data = []
    for i in range(1, file_count+1):
        data = data + pattern.findall(nltk.data.load(path+complete_id(i), format='text'))

    # from every tag form the list find the two substrings
    # that correspond to the snd_pattern
    raw_entities = [list(map(lambda s: (s[:len(s)-1])[1:], l)) for l in (re.findall(snd_pattern, tag) for tag in data)]

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
    print(word_list.words('wsj_0001.txt'))
    print(word_list.sents('wsj_0012.txt'))
    return word_list

path = '/Users/adrian_radulescu1997/Documents/Uni-Courses/Natural Language Processing/wsj_training/'
file_count = 2000

ren = tag_reading_and_entity_extraction(path, file_count)

print(ren)

path1 = '/Users/adrian_radulescu1997/Documents/Uni-Courses/Natural Language Processing/wsj_untagged/'
