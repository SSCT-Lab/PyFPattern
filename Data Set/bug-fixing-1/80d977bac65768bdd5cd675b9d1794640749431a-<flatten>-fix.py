

def flatten(mylist, levels=None):
    ret = []
    for element in mylist:
        if (element in (None, 'None', 'null')):
            break
        elif is_sequence(element):
            if (levels is None):
                ret.extend(flatten(element))
            elif (levels >= 1):
                ret.extend(flatten(element, levels=(int(levels) - 1)))
            else:
                ret.append(element)
        else:
            ret.append(element)
    return ret
