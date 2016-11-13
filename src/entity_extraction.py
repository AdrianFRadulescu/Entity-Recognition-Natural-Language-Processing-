import nltk
import re
from src.tagging import tag, final_tagger,concat


def dbpedia_filter():

    return []


def tagged_corpud_filter():

    return []


def candidate_filter(candidates):

    """

    :param candidates: the candidates for entities
    :return: a list of candidates that match an entity in the corpus or on dbpedia

    """
    #return filter(lambda x: #data.find() , candidates)
    return []


def sent_entities(sent=None):

    """
    :param sent: a sentence(represented as a list of tokens)
                 from which the entities must be extracted
    :return:     a list of noun phrases representing the candidates for entities
    """

    # tag each sentence
    # extract the groups of consecutive nouns and determiners

    tagger = final_tagger()


    str_tagged_sent = \
        concat(
            list(
                map(
                    lambda x: " " + str(x[0]) + "->" + str(x[1]),
                    tagger.tag(sent)
                )
            )
        )

    print("str_tagged_sent= "+str_tagged_sent)

    # (Adjective | Noun)* (Noun Preposition)? (Adjective | Noun)* Noun - the ideal pattern

    # group extraction patterns
    gep = [
        re.compile(r'((?:\s\w+->(?:DT|JJ|NNPS|NNP|NNS|NN))*(?:\sof->IN)?\s\w+->(?:NNPS|NNP|NNS|NN))', re.ASCII),
        re.compile(r'(?:\s\w+->(?:NNPS|NNP|NNS|NN))+', re.ASCII),
        re.compile(r'\w+->DT\s(?:\s\w+->(?:NNPS|NNP|NNS|NN))+')
    ]

    # words extraction patern from the results of the previous extraction
    wep = re.compile(r'\w+(?=->)', re.ASCII)
    # POS extraction pattern from the results of the previous extraction
    POSex = re.compile(r'(?<=->)\w+', re.ASCII)

    candidate_entities = []
    for p in gep:
        candidate_entities += list(map(lambda x: list(zip(wep.findall(x), POSex.findall(x))), p.findall(str_tagged_sent)))

    # evaluate each entity against the corpus data and dbpedia

    print("cand")
    print(candidate_entities[:100])

    return candidate_filter(candidates=candidate_entities)


def corpus_entities(corpus=None):

    rez = []
    for sent in corpus.sents():
        rez += sent_entities(sent)

    return rez


def test_sent_entities(sent=None):

    print(sent)
    sent_entities(sent)