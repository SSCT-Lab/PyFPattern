def rename_item_if_exists(dict_object, attribute, new_attribute, child_node=None, attribute_type=None):
    new_item = dict_object.get(attribute)
    if (new_item is not None):
        if (attribute_type is not None):
            new_item = attribute_type(new_item)
        if (child_node is None):
            dict_object[new_attribute] = new_item
        else:
            dict_object[child_node][new_attribute] = new_item
        dict_object.pop(attribute)
    return dict_object