def dumps(objects, output='block'):
    if (output == 'block'):
        item = _obj_to_raw(objects)
    elif (output == 'commands'):
        items = _obj_to_text(objects)
    else:
        raise TypeError('unknown value supplied for keyword output')
    return '\n'.join(items)