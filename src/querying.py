
from nltk.classify import NaiveBayesClassifier
from nltk.tag import StanfordPOSTagger

from src.tagging import final_tagger
from nltk.tokenize import word_tokenize


class OrganizationDictionary(object):

    def __init__(self):

        self.__pos_dict = {}

    def insert(self, entity, label):

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

        print(entity)

        self.__update(entity)

        print(entity[-1])

        print(self.__pos_dict[entity[-1][1]][entity[-1][0]])
        self.__pos_dict[entity[-1][1]][entity[-1][0]].add_label(label)

        print()

    def __update(self, entity):

        '''
            Check if all the words are already in the dictionary
            For the ones that are not then create and add them
        :param entity: the entity containing the words and the corresponding POS
        '''

        for (word, pos) in entity:
            if pos not in self.__pos_dict:
                # create a new node and add it to the dictionary
                self.__pos_dict[pos] = {}
                self.__pos_dict[pos][word] = self.__Node(word)
            else:
                if word not in self.__pos_dict[pos]:
                    # create a new node and add it to the dictionary
                    self.__pos_dict[pos][word] = self.__Node(word)

    def entities(self):

        '''
        :return: a dictionary containing the entities in the data structures
        '''

        return self.__pos_dict

    class __Node(object):

        '''
            A wrapper around a word containing the word and the links
            to the other words that follow it in their common entities
        '''

        def __init__(self, word=None, links=[], labels=[]):

            '''

            :param word: the actual word
            :param links: a list of Node objects pointing to the words that are
                right after word in the entities where word appears
            :param is_entity: a pointer towards the actual entity containing the word
            '''

            self.__word = word
            self.__links = links
            self.__labels = labels

        def links(self):

            '''
            :return: the links to all the words that follow this one(with the corresponding pos)
            '''

            return self.__links

        def word(self):

            '''
            :return: the word contained in the node object
            '''

            return self.__word

        def add_label(self, l):
            self.__labels += [l]

        def get_labels(self):
            return self.__labels

        def union(self, wn):
            '''
                if two nodes have the same word then unite the links
            :param wn:
            :return:
            '''
            self.__links =self.__links + wn.links()

        def __eq__(self, wn):
            return self.__word == wn.word()

        def __repr__(self):
            return "__Node("+str(self.__word) + "," + str(self.__links) + "," + str(self.__labels) + ")"

        def __str__(self):
            return "Node :" +" "+str(self.__word) + " " + str(self.__links) + " " + str(self.__labels)

    def labels(self, pos, word):
        return self.__pos_dict[pos][word].get_labels()