

def parameterize_pytest(names, values):
    assert isinstance(names, str)
    assert isinstance(values, (tuple, list))

    def safe_zip(ns, vs):
        if (len(ns) == 1):
            return [(ns[0], vs)]
        assert (isinstance(vs, (tuple, list)) and (len(ns) == len(vs)))
        return zip(ns, vs)
    names = names.split(',')
    params = [dict(safe_zip(names, value_list)) for value_list in values]
    return parameterize(*params)
