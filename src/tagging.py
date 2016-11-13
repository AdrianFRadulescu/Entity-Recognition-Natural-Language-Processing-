from brill_tagger_wrapper import train_brill_tagger


from nltk.corpus import brown,treebank,reuters
from src.files_reading import untagged_reading

from nltk.tag import BrillTagger
from nltk.tag import BigramTagger
from nltk.tag import TrigramTagger
from nltk.tag import UnigramTagger
from nltk.tag import DefaultTagger
from nltk.tag import PerceptronTagger

import re
import name_tagger
from brill_tagger_wrapper import train_brill_tagger

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

tagger = final_tagger()


# (Adjective | Noun)* (Noun Preposition)? (Adjective | Noun)* Noun

# almost perfect
pattern7 = re.compile(r'((?:\s\w+->(?:DT|JJ|NNPS|NNP|NNS|NN))*(?:\sof->IN)?\s\w+->(?:NNPS|NNP|NNS|NN))', re.ASCII)

# extracts groups of nouns
pattern8 = re.compile(r'(?:\s\w+->(?:NNPS|NNP|NNS|NN))+', re.ASCII)

# extracts groups of nouns preceded by determiners
pattern9 = re.compile(r'\w+->DT\s(?:\s\w+->(?:NNPS|NNP|NNS|NN))+')

str_tagged_sent = \
    concat(
        list(
            map(
                lambda x: " "+str(x[0])+"->"+str(x[1]),
                tag("The National Association of Manufacturers settled on the Hoosier capital of Indianapolis for its fall board meeting".split())
            )
        )
    )

print(str_tagged_sent)
print('pattern7')
print(pattern7.findall(str_tagged_sent))
print('pattern8')
print(pattern8.findall(str_tagged_sent))
print('pattern9')
print(pattern9.findall(str_tagged_sent))


wep = re.compile(r'\w+(?=->(?:DT|JJ|NNPS|NNP|NNS|NN|IN))', re.ASCII)
POSex = re.compile(r'(?<=->)\w+', re.ASCII)

l = list(map(lambda x: list(zip(wep.findall(x), POSex.findall(x))), pattern7.findall(str_tagged_sent)))

print(l)
print()
print()

#print(pattern.findall(str_tagged_sent))

