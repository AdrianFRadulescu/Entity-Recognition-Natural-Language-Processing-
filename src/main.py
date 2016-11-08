
from src.files_reading import tag_reading_and_entity_extraction
from src.files_reading import untagged_reading

path = '/Users/adrian_radulescu1997/Documents/Uni-Courses/Natural Language Processing/wsj_training/'
file_count = 2000


entities = tag_reading_and_entity_extraction(path, file_count)


print(entities)