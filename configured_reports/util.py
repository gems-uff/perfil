def append_lists(list_1, list_2):
    """Appends the two lists in a new list using the list.extend() built-in function"""

    new_list = list_1.copy()
    new_list.extend(list_2)
    return new_list
