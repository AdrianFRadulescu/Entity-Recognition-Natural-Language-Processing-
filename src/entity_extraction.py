import re
import src.globl

from src.tagging import final_tagger, concat
from src.wikification import find_inf
from nltk.corpus import names
from nltk.tokenize import word_tokenize

def wikipedia_filter(entity=None):

    inf = find_inf(entity)

    return []


def tagged_corpus_filter(candidate=None):

    """
    :param candidate: the entity that is to be searched in the tagged entities data structures
    :return: true if there is a match for the given candidate
             false otherwise
    """

    potential = {}

    candidate = list(map(lambda x: x[0].lower(), candidate))

    # check if the candidate has common words with the entities in the list(at least the most frequent words)

    '''
    if any(map(lambda t: t in src.globl.org_tokens, candidate)):
        potential['ORGANIZATION'] = True
    if any(map(lambda t: t in src.globl.name_data or t in names.words(), candidate)):
        potential['PERSON'] = True
    if any(map(lambda t: t in src.globl.loc_tokens, candidate)):
        potential['LOCATION'] = True

    result = False
    if any(potential):
        # it's worth searching for the entity in the current data

        for (label,name) in list(filter(lambda re: potential[re[0]],src.globl.entity_data)):

            e_tokens = set(word_tokenize(name))
            if e_tokens.issubset(set(candidate)) or e_tokens.issuperset(set(candidate)):
                result = True
    '''

    result = False

    if any(map(lambda t: t[0] in src.globl.org_tokens and t in src.globl.org_tokens[t[0]], candidate)):
        potential['ORGANIZATION'] = True
    if any(map(lambda t: t[0] in src.globl.name_data and t in src.globl.name_data, candidate)):
            potential['PERSON'] = True
    if any(map(lambda t: t[0] in src.globl.loc_tokens and t in src.globl.loc_tokens[t[0]] , candidate)):
        potential['LOCATION'] = True

    result = any(potential)

    return result


def candidate_filter(candidates=None):

    """

    :param candidates: the candidates for entities
    :return: a list of candidates that match an entity in the corpus or on dbpedia

    """
    entities = []
    for candidate in candidates:
        if tagged_corpus_filter(candidate):
            entities +=[candidate]

    return entities


def sent_entities(sent=None):

    """
    :param sent: a sentence(represented as a list of tokens)
                 from which the entities must be extracted
    :return:     a list of noun phrases representing the candidates for entities
    """

    # tag each sentence
    # extract the groups of consecutive nouns and determiners

    str_tagged_sent = \
        concat(
            list(
                map(
                    lambda x: " " + str(x[0]) + "->" + str(x[1]),
                    src.globl.tagger.tag(sent)
                )
            )
        )

    # (Adjective | Noun)* (Noun Preposition)? (Adjective | Noun)* Noun - the ideal pattern

    # group extraction patterns
    gep = [
        re.compile(r'((?:\s\w+->(?:DT|JJ|NNPS|NNP|NNS|NN))*(?:\sof->IN)?\s\w+->(?:NNPS|NNP|NNS|NN))', re.ASCII),
        re.compile(r'(?:\s\w+->(?:NNPS|NNP|NNS|NN))+', re.ASCII),
        re.compile(r'\w+->DT\s(?:\s\w+->(?:NNPS|NNP|NNS|NN))+'),
        re.compile(r'Mr[.]->\w+\s(?:\s\w+->(?:NNPS|NNP|NNS|NN))+')
    ]

    # words extraction patern from the results of the previous extraction
    wep = re.compile(r'\w+(?=->)', re.ASCII)
    # POS extraction pattern from the results of the previous extraction
    POSex = re.compile(r'(?<=->)\w+', re.ASCII)

    candidate_entities = []
    for p in gep:
        candidate_entities += list(map(lambda x: list(zip(wep.findall(x), POSex.findall(x))), p.findall(str_tagged_sent)))

    # evaluate each entity against the corpus data and wikipedia

    return candidate_filter(candidates=candidate_entities)


def corpus_entities(corpus=None):

    rez = []

    sents = corpus.sents()

    #rez += list(map(lambda s : sent_entities(s), sents[:-1]))

    i = 0

    for fi in corpus.fileids():

        if corpus.raw(fileids=fi) == "":
            break
        for sent in corpus.sents(fileids=fi):
            try:
                rez += sent_entities(sent)
            except TypeError:
                continue
    return rez
