def search_obj_in_list(name, lst, key='name'):
    for item in lst:
        if (item[key] == name):
            return item
    return None