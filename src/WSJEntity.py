from nltk.corpus.reader.wordnet import NOUN


class WSJEntity(object):

        def __init__(self, args=None):

            """
            :param args: a list where the first is the type and the second is the actual name of the entity

            """

            self._type = args[0]
            self._name = args[1]
            self._composition = []

        def type(self):
            return self._type

        def change_type(self, _new_type):
            self._type = _new_type