def rename_item_if_exists(dict_object, attribute, new_attribute, child_node=None):
    new_item = dict_object.get(attribute)
    if (new_item is not None):
        if (child_node is None):
            dict_object[new_attribute] = dict_object.get(attribute)
        else:
            dict_object[child_node][new_attribute] = dict_object.get(attribute)
        dict_object.pop(attribute)
    return dict_object