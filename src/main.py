
from src.files_reading import training_data
from src.files_reading import untagged_reading
from src.entity_extraction import sent_entities
from src.entity_extraction import test_sent_entities

paths = [
    '/Users/adrian_radulescu1997/Documents/Uni-Courses/Natural Language Processing/wsj_training/',
    '/Users/adrian_radulescu1997/Documents/Uni-Courses/Natural Language Processing/Entity-Recognition-Natural-Language-Processing-/training_data',
    '/Users/adrian_radulescu1997/Documents/Uni-Courses/Natural Language Processing/wsj_untagged'
]

file_count = 10

#entity_data = training_data(paths, file_count)

untagged = untagged_reading(paths[2])

for x in range(0,10):

    test_sent_entities(untagged.sents()[x])


