import pickle
import src.tagging

"""
    A file containing all the extraction form the training data(tagged files)
    and the final tagger to be used in the entity extraction
"""


entity_data = pickle.load(open('raw_labeled_data.pkl', 'rb'))

org_tokens = pickle.load(open('organization_data.pkl', 'rb'))

name_data = pickle.load(open('name_data.pkl', 'rb'))

loc_tokens = pickle.load(open('loc_data.pkl', 'rb'))

tagger = src.tagging.final_tagger()
