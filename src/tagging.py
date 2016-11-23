
import re
import name_tagger
from brill_tagger_wrapper import train_brill_tagger

from nltk.corpus import brown,treebank,reuters

from nltk.tag import BigramTagger
from nltk.tag import TrigramTagger
from nltk.tag import UnigramTagger


from nltk.tag import pos_tag


def tag(args):
    return pos_tag(args)


def concat(args):
    rez = args[0]
    for a in args[1:]:
        rez += a
    return rez


def backoff_tagger(train_sents, tagger_classes, backoff=None):
    for cls in tagger_classes :
          backoff = cls(train_sents, backoff=backoff)
    return backoff


def final_tagger():

    train_sents = treebank.tagged_sents()
    tagger = backoff_tagger(train_sents, [UnigramTagger, BigramTagger, TrigramTagger], backoff=name_tagger.NamesTagger())
    tagger = train_brill_tagger(tagger, train_sents)

    return tagger

