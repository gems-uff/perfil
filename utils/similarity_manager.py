from difflib import SequenceMatcher


def get_similarity(text_one, text_two):
    '''Auxiliar function to do the lcs calculations'''
    return SequenceMatcher(None, text_one, text_two).ratio()


def detect_similar(text, texts_to_compare, minimum_similarity, similarity_dict):
    '''Tries to detect similar texts from texts received'''

    if minimum_similarity == 1: return None

    similarity_found = 0
    similar_text_in_dict = None

    for dict_text_to_check in texts_to_compare:
        if type(dict_text_to_check) == str:
            similarity = get_similarity(text.upper(), dict_text_to_check.upper())
            if similarity >= minimum_similarity and similarity >= similarity_found:
                similarity_found = similarity
                similar_text_in_dict = dict_text_to_check

    if similar_text_in_dict is not None: add_similar_to_dict(text, similarity_dict, similar_text_in_dict)

    return similar_text_in_dict


def add_similar_to_dict(text, dictionary, value):
    '''Auxiliar function to add a new entry to the similarity text dict'''
    if text not in dictionary:
        dictionary[text] = value
