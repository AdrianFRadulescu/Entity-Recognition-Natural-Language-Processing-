
import pickle
from src.file_reading import training_data
from src.file_reading import untagged_reading
from src.entity_extraction import sent_entities,corpus_entities
from src.entity_extraction import corpus_entities
from nltk.corpus import names

from src.enitity_classifier import organization_classifier, org_features, specifics
from src.wikification import find_inf

from src.tagging import concat

paths = [
    '/Users/adrian_radulescu1997/Documents/Uni-Courses/Natural Language Processing/wsj_training/',
    '/Users/adrian_radulescu1997/Documents/Uni-Courses/Natural Language Processing/Entity-Recognition-Natural-Language-Processing-/training_data',
    '/Users/adrian_radulescu1997/Documents/Uni-Courses/Natural Language Processing/wsj_untagged'
]


'''
    To save time I store the data gained from the tagged data
    in a pickle file and the loaded them in globl.py
'''

'''
entity_dict, org_tokens_dict, name_dict,loc_dict = training_data(paths)


pickle.dump(entity_dict, open('raw_labeled_data.pkl', 'wb'))
pickle.dump(org_tokens_dict,open('organization_data.pkl', 'wb'))
pickle.dump(name_dict,open('name_data.pkl', 'wb'))
pickle.dump(loc_dict,open('loc_data.pkl', 'wb'))
'''

untagged = untagged_reading(paths[2])

entites = corpus_entities(untagged)

for e in entites:
    print(e)
print(len(entites))

