
from nltk.tag import DefaultTagger
from nltk.tag import UnigramTagger,BigramTagger,TrigramTagger,TnT
from nltk.tag import brill,brill_trainer

def backoff_tagger(train_sents, tagger_classes, backoff=None,cutoff=None):
    for cls in tagger_classes:
        backoff = cls(train_sents, backoff=backoff)
    return backoff