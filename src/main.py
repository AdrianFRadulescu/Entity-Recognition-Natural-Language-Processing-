

from src.files_reading import training_data
from src.files_reading import untagged_reading
#from src.entity_extraction import sent_entities
from src.entity_extraction import test_sent_entities


from src.wikification import find_inf

paths = [
    '/Users/adrian_radulescu1997/Documents/Uni-Courses/Natural Language Processing/wsj_training/',
    '/Users/adrian_radulescu1997/Documents/Uni-Courses/Natural Language Processing/Entity-Recognition-Natural-Language-Processing-/training_data',
    '/Users/adrian_radulescu1997/Documents/Uni-Courses/Natural Language Processing/wsj_untagged'
]

file_count = 3


wsj_tagged_entity_data, name_data = training_data(paths, file_count)

d = {'a':{'a':2}}

print(d['a']['a'])

d['a']['a']=3
print(d['a']['a'])

d['a']['b'] =1
print(d)

#untagged = untagged_reading(paths[2])
