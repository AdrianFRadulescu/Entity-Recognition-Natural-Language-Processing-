
from nltk import FreqDist
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from nltk.corpus import names


def org_features(ent_name=None,specifics=None):

    '''
        Build the feature dictionary of an entity based on its length and
         appearance of common organization components such as "Corp.","Co.","Ltd"
    :param ent_name: the name of the entity
    :param specifics:
    :return:
    '''

    features = {}

    # tokenize the entity
    ent_name = word_tokenize(ent_name)
    features['length_is_greater than 2'] = len(ent_name) > 2
    for word in specifics:
        features['has({})'.format(word)] = word in ent_name


    features['person_name'] = filter(lambda x: x in names.words(),ent_name) != []

    return features


def specifics(entities=None):

    # extract the words from the organizations in the training data

    words = []
    for ent in entities:
        if ent[0] == 'ORGANIZATION':
            words += word_tokenize(ent[1])

    # use the most common in order to create feature sets
    print(FreqDist(words).most_common(10))
    return FreqDist(words).most_common(10)


def organization_classifier(entities=None,specs=None):

    if specs is None:
        specs = specifics(entities=entities)

    return NaiveBayesClassifier.train([(org_features(ent_name=n, specifics=specs), l == 'ORGANIZATION') for (l,n) in entities])