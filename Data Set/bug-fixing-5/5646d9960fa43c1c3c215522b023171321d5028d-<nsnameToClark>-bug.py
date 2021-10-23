def nsnameToClark(name, namespaces):
    if (':' in name):
        (nsname, rawname) = name.split(':')
        return '{{{0}}}{1}'.format(namespaces[nsname], rawname)
    else:
        return name