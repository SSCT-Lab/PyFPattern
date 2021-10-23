def dumps(objects, output='block', comments=False):
    if (output == 'block'):
        items = _obj_to_block(objects)
    elif (output == 'commands'):
        items = _obj_to_text(objects)
    else:
        raise TypeError('unknown value supplied for keyword output')
    if (output != 'commands'):
        if comments:
            for (index, item) in enumerate(items):
                nextitem = (index + 1)
                if ((nextitem < len(items)) and (not item.startswith(' ')) and items[nextitem].startswith(' ')):
                    item = ('!\n%s' % item)
                items[index] = item
            items.append('!')
        items.append('end')
    return '\n'.join(items)