def sub(content, delimeters=None, **kw):
    name = kw.get('__name')
    tmpl = Template(content, name=name, delimeters=delimeters)
    return tmpl.substitute(kw)