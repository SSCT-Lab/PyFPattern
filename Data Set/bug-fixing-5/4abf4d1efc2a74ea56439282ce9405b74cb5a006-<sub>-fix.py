def sub(content, delimiters=None, **kw):
    name = kw.get('__name')
    tmpl = Template(content, name=name, delimiters=delimiters)
    return tmpl.substitute(kw)