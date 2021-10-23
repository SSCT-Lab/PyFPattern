def get_dict_of_struct(struct, connection=None, fetch_nested=False, attributes=None):
    '\n    Convert SDK Struct type into dictionary.\n    '
    res = {
        
    }

    def remove_underscore(val):
        if val.startswith('_'):
            val = val[1:]
            remove_underscore(val)
        return val

    def convert_value(value):
        nested = False
        if isinstance(value, sdk.Struct):
            return get_dict_of_struct(value)
        elif (isinstance(value, Enum) or isinstance(value, datetime)):
            return str(value)
        elif (isinstance(value, list) or isinstance(value, sdk.List)):
            if (isinstance(value, sdk.List) and fetch_nested and value.href):
                try:
                    value = connection.follow_link(value)
                    nested = True
                except sdk.Error:
                    value = []
            ret = []
            for i in value:
                if isinstance(i, sdk.Struct):
                    if (not nested):
                        ret.append(get_dict_of_struct(i))
                    else:
                        nested_obj = dict(((attr, convert_value(getattr(i, attr))) for attr in attributes if getattr(i, attr, None)))
                        nested_obj['id'] = getattr(i, 'id', None)
                        ret.append(nested_obj)
                elif isinstance(i, Enum):
                    ret.append(str(i))
                else:
                    ret.append(i)
            return ret
        else:
            return value
    if (struct is not None):
        for (key, value) in struct.__dict__.items():
            if (value is None):
                continue
            key = remove_underscore(key)
            res[key] = convert_value(value)
    return res