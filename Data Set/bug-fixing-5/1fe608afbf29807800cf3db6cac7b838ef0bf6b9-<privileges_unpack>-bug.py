def privileges_unpack(priv, mode):
    " Take a privileges string, typically passed as a parameter, and unserialize\n    it into a dictionary, the same format as privileges_get() above. We have this\n    custom format to avoid using YAML/JSON strings inside YAML playbooks. Example\n    of a privileges string:\n\n     mydb.*:INSERT,UPDATE/anotherdb.*:SELECT/yetanother.*:ALL\n\n    The privilege USAGE stands for no privileges, so we add that in on *.* if it's\n    not specified in the string, as MySQL will always provide this by default.\n    "
    if (mode == 'ANSI'):
        quote = '"'
    else:
        quote = '`'
    output = {
        
    }
    privs = []
    for item in priv.strip().split('/'):
        pieces = item.strip().split(':')
        dbpriv = pieces[0].rsplit('.', 1)
        for (i, side) in enumerate(dbpriv):
            if (side.strip('`') != '*'):
                dbpriv[i] = ('%s%s%s' % (quote, side.strip('`'), quote))
        pieces[0] = '.'.join(dbpriv)
        if ('(' in pieces[1]):
            output[pieces[0]] = re.split(',\\s*(?=[^)]*(?:\\(|$))', pieces[1].upper())
            for i in output[pieces[0]]:
                privs.append(re.sub('\\s*\\(.*\\)', '', i))
        else:
            output[pieces[0]] = pieces[1].upper().split(',')
            privs = output[pieces[0]]
        new_privs = frozenset(privs)
        if (not new_privs.issubset(VALID_PRIVS)):
            raise InvalidPrivsError(('Invalid privileges specified: %s' % new_privs.difference(VALID_PRIVS)))
    if ('*.*' not in output):
        output['*.*'] = ['USAGE']
    if (('REQUIRESSL' in priv) and (not set(output['*.*']).difference(set(['GRANT', 'REQUIRESSL'])))):
        output['*.*'].append('USAGE')
    return output