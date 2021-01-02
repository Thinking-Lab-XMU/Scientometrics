import spacy
import datetime
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
import random
import pandas as pd


def get_special_dict(file_name, column_name):
    """
    Get dictionary
    :param file_name: Dictionary excel file name
    :param column_name: Column name of dictionary data
    :return:
    """
    data = pd.read_excel(file_name)
    data[column_name] = data[column_name].apply(lambda x: x.lower())
    return list(set(list(data[column_name])))


def dict_to_list(entity_dict):
    """
    Convert the entity dictionary stored in the form of a dictionary into a list (not repeated)
    :param entity_dict:
    :return:
    """
    entity_set = []
    for key, value in entity_dict.items():
        # if key == 'ID' or key == 'DE':
        #     continue
        entity_set = entity_set + value
    entity_set = set(entity_set)
    entity_set = list(entity_set)

    return entity_set


def transform_dict_to_spacy(entity_dict):
    """
    Convert the dictionary to spacy's dictionary format
    :param entity_dict: Entity dictionary
    :return:
    """
    patterns = []
    for key, value in entity_dict.items():
        # for i in range(10):
        for i in range(len(value)):
            list_item = {}
            list_item['label'] = key.upper()
            list_item['id'] = value[i]
            pattern_list = []
            for word in value[i].split():
                pattern_list_item = {"LOWER" : word.lower()}
                pattern_list.append(pattern_list_item)
            list_item['pattern'] = pattern_list
            patterns.append(list_item)

    return patterns


def spacy_ner_basedon_dict_2(rows, patterns):
    """
    Dictionary-based annotation
    :param rows:
    :param patterns:
    :return:
    """
    nlp = English()
    ruler = EntityRuler(nlp)
    ruler.add_patterns(patterns)
    nlp.add_pipe(ruler)
    entities = []
    doc = nlp(rows)
    if len(doc.ents) != 0:
        entities = [(ent.start_char, ent.end_char, ent.text.lower()) for ent in doc.ents]
    return entities









