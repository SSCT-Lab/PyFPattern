

def re_matchall(regex, value):
    objects = list()
    for match in re.findall(regex.pattern, value, re.M):
        obj = {
            
        }
        if regex.groupindex:
            for (name, index) in iteritems(regex.groupindex):
                obj[name] = match[(index - 1)]
            objects.append(obj)
    return objects
