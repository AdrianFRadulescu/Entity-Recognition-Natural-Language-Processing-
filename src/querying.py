
from nltk.classify import NaiveBayesClassifier
from nltk.tag import StanfordPOSTagger

from src.tagging import final_tagger
from nltk.tokenize import word_tokenize


class DataStructure(object):

    def __init__(self):

        self.__pos_dict = {}

    def insert(self, entity,label):

        '''
            Inserts an entity given as a string of words(untagged) into the pos_dictionaries
            by tagging each word of the entity assigning it to its right place in the dictionary
            wrapped in an EntityNone and establishes the links between the words of the same
            entity

        :param entity: the string representing the name of the entity
        :param label: the label given to the entity
        :return:
        '''

        print(entity)
        print(label)

        entity = final_tagger().tag(word_tokenize(entity))

        for tag in entity:
            self.__update(tag[1], tag[0], None)

        #for index in range(0,len(entity)-2):

    def __update(self, pos, name, node=None):

        '''
            Update the dictionary for the given part of POS
            in case the POS was not encountered yet create a new place in the dictionary
            otherwise check if the nodes wrap the same word.If yes then add the links to the existing node,otherwise
            ad the node to the list
        :param pos:
        :param node:
        :return:
        '''

        if pos in self.__pos_dict:

            if name not in self.__pos_dict[pos]:
                self.__pos_dict[pos][name] = self.__WordNode(name)
            else:
                self.__pos_dict[pos][name].union(node)
        else:
            self.__pos_dict[pos] = {name:self.__WordNode(name)}

    def entities(self):

        '''
        :return: a dictionary containing the entities in the data structures
        '''

        return self.__pos_dict

    def test(self):

        x1 = self.__WordNode(val='mama')
        x2 = self.__WordNode(val='mama',links=[x1])

        x1.union(x2)

        print(x1 in x1.links())

    class __WordNode(object):

        def __init__(self, val=None, links=[], is_entity=False):

            self.__val = val
            self.__links = links
            self.__is_entity = is_entity

        def links(self):
            return self.__links

        def val(self):
            return self.__val

        def union(self, wn):
            self.__links =self.__links + wn.links()

        def __eq__(self, wn):
            return self.__val == wn.val()

        def __repr__(self):
            return "__WordNode("+str(self.__val) + "," + str(self.__links) + ")"

        def __str__(self):
            return str(self.__val) + " " + str(self.__links)